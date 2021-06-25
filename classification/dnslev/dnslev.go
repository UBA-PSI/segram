package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"runtime"
)

type PacketType int

const (
	TYPE_MSG PacketType = iota
	TYPE_GAP            = iota
)

type VectorJSON struct {
	Traces []struct {
		AppName  string          `json:"app_name"`
		Sequence [][]interface{} `json:"dns_seq"`
	} `json:"dns_sequences"`
}

type ResultJSON struct {
	Results []*DistanceResult `json:"results"`
}

type Packet struct {
	Type  PacketType
	Value uint64
}

type PacketTrace struct {
	AppName  string
	Sequence []Packet
}

type vectorMemoIndex struct {
	i uint64
	j uint64
}

type DistanceResult struct {
	I        int    `json:"i"`
	J        int    `json:"j"`
	Distance uint64 `json:"distance"`
}

func diff(x, y uint64) uint64 {
	if x < y {
		return y - x
	} else {
		return x - y
	}
}

func min(x, y uint64) uint64 {
	if x < y {
		return x
	} else {
		return y
	}
}

func Distance(vecA, vecB []Packet) uint64 {
	memo := make(map[vectorMemoIndex]uint64)
	costs := distanceMemo(vecA, vecB, 0, 0, memo)
	return costs
}

func distanceMemo(vecA, vecB []Packet, i, j uint64, memo map[vectorMemoIndex]uint64) uint64 {
	memoIndex := vectorMemoIndex{i, j}
	x, ok := memo[memoIndex]
	if ok {
		return x
	}

	if len(vecA) == 0 {
		costs := calculateVectorCosts(vecB)
		memo[memoIndex] = costs
		return costs
	} else if len(vecB) == 0 {
		costs := calculateVectorCosts(vecA)
		memo[memoIndex] = costs
		return costs
	} else if vecA[0].Type == vecB[0].Type && vecA[0].Value == vecB[0].Value {
		costs := distanceMemo(vecA[1:], vecB[1:], i+1, j+1, memo)
		memo[memoIndex] = costs
		return costs
	} else {
		deleteCosts := uint64(0)
		if vecA[0].Type == TYPE_MSG {
			deleteCosts = 12
		} else if vecA[0].Type == TYPE_GAP {
			deleteCosts = vecA[0].Value
		} else {
			panic("Unexpected case.")
		}
		deleteCosts += distanceMemo(vecA[1:], vecB, i+1, j, memo)

		insertCosts := uint64(0)
		if vecB[0].Type == TYPE_MSG {
			insertCosts = 12
		} else if vecB[0].Type == TYPE_GAP {
			insertCosts = vecB[0].Value
		} else {
			panic("Unexpected case.")
		}
		insertCosts += distanceMemo(vecA, vecB[1:], i, j+1, memo)

		substCosts := uint64(0)
		a := vecA[0]
		b := vecB[0]
		if a.Type == TYPE_MSG && b.Type == TYPE_MSG {
			substCosts = (12 + 12) / 4
		} else if a.Type == TYPE_GAP && b.Type == TYPE_GAP {
			substCosts = diff(a.Value, b.Value) * 3
		} else if a.Type == TYPE_MSG && b.Type == TYPE_GAP {
			substCosts = 12 + b.Value
		} else if a.Type == TYPE_GAP && b.Type == TYPE_MSG {
			substCosts = a.Value + 12
		} else {
			panic("Unexpected case.")
		}
		substCosts += distanceMemo(vecA[1:], vecB[1:], i+1, j+1, memo)

		costs := min(deleteCosts, min(insertCosts, substCosts))

		// Swap costs must come after all costs, because they consume two characters
		// and are not always applicable.
		if len(vecA) > 1 && len(vecB) > 1 {
			if isSamePacket(vecA[1], vecB[0]) && isSamePacket(vecA[0], vecB[1]) {
				swapCosts := 3 + distanceMemo(vecA[2:], vecB[2:], i+2, j+2, memo)
				costs = min(costs, swapCosts)
			}
		}

		memo[memoIndex] = costs
		return costs
	}
}

func isSamePacket(a, b Packet) bool {
	return a.Type == b.Type && a.Value == b.Value
}

func calculateVectorCosts(vec []Packet) uint64 {
	costs := uint64(0)
	for _, packet := range vec {
		if packet.Type == TYPE_MSG {
			costs += 12
		} else if packet.Type == TYPE_GAP {
			costs += packet.Value
		} else {
			panic("Unexpected case.")
		}
	}
	return costs
}

func loadTraces(filename string) []PacketTrace {
	jsonFile, err := os.Open(filename)
	if err != nil {
		panic("No such JSON file.")
	}
	defer jsonFile.Close()
	content, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		panic("Could not read JSON file.")
	}
	jsonVectors := VectorJSON{}
	err = json.Unmarshal(content, &jsonVectors)
	if err != nil {
		panic("Invalid JSON")
	}
	traceList := make([]PacketTrace, 0)
	for _, trace := range jsonVectors.Traces {
		sequence := make([]Packet, 0)
		for _, elem := range trace.Sequence {
			tStr := elem[0].(string)
			x := elem[1].(float64)
			var val uint64
			if x < 0 {
				val = uint64(-x)
			} else {
				val = uint64(x)
			}
			var t PacketType
			if tStr == "M" {
				t = TYPE_MSG
			} else if tStr == "G" {
				t = TYPE_GAP
			} else {
				panic("Invalid type found in JSON.")
			}
			sequence = append(sequence, Packet{t, val})

		}
		traceList = append(traceList, PacketTrace{AppName: trace.AppName, Sequence: sequence})
	}
	return traceList
}

func startWorker(traces []PacketTrace, jobQueue chan *DistanceResult, quit chan int) {
	for job := range jobQueue {
		traceA := traces[job.I]
		traceB := traces[job.J]
		costs := Distance(traceA.Sequence, traceB.Sequence)
		job.Distance = costs
	}
	quit <- 1
}

func sendJobs(jobQueue chan *DistanceResult, results []*DistanceResult) {
	for total, result := range results {
		jobQueue <- result
		if total%10000 == 0 {
			max := float64(len(results))
			perc := float64(total) / max * 100.0
			fmt.Fprintf(os.Stderr, "%d; %.4f %%\n", total, perc)
		}
	}
	close(jobQueue)
}

func main() {
	filename := os.Args[1]
	numWorkers := runtime.NumCPU()
	runtime.GOMAXPROCS(numWorkers)
	traces := loadTraces(filename)
	results := make([]*DistanceResult, 0)
	jobQueue := make(chan *DistanceResult)
	quit := make(chan int)

	for i := 0; i < len(traces); i++ {
		for j := 0; j < len(traces); j++ {
			if i > j {
				continue
			} else {
				result := new(DistanceResult)
				result.I = i
				result.J = j
				results = append(results, result)
			}
		}
	}

	for i := 0; i < numWorkers; i++ {
		go startWorker(traces, jobQueue, quit)
	}
	go sendJobs(jobQueue, results)
	for numWorkers > 0 {
		<-quit
		numWorkers -= 1
	}
	writer, err := os.Create(filename + "-distances.json")
	if err != nil {
		panic(err)
	}
	defer writer.Close()
	enc := json.NewEncoder(writer)

	if err := enc.Encode(ResultJSON{results}); err != nil {
		panic(err)
	}
	//vecA := []Packet{Packet{TYPE_MSG, 230}, Packet{TYPE_GAP, 5}, Packet{TYPE_MSG, 350}}
	//vecB := []Packet{Packet{TYPE_MSG, 230}, Packet{TYPE_GAP, 4}, Packet{TYPE_MSG, 350}}
}
