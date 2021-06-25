package main

import (
	"testing"
)

func TestDistance(t *testing.T) {
	seqx := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	seq0 := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	seq1 := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	seq2 := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	seq3 := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	seq4 := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 936}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	seq5 := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 8}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	seq6 := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 5}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	seq7 := []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}}
	seq8 :=  []Packet{Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}, Packet{TYPE_MSG, 468}, Packet{TYPE_GAP, 12}, Packet{TYPE_MSG, 468}}
	var got uint64
	got = Distance(seqx, seq0)
	if Distance(seqx, seq0) != 12 {
		t.Errorf("Distance(seqx, seq0) = %d; want 12", got)
	}

	got = Distance(seqx, seq1)
	if Distance(seqx, seq1) != 12 {
		t.Errorf("Distance(seqx, seq1) = %d; want 12", got)
	}

	got = Distance(seqx, seq2)
	if Distance(seqx, seq2) != 12 {
		t.Errorf("Distance(seqx, seq2) = %d; want 12", got)
	}

	got = Distance(seqx, seq3)
	if Distance(seqx, seq3) != 12 {
		t.Errorf("Distance(seqx, seq3) = %d; want 12", got)
	}

	got = Distance(seqx, seq4)
	if Distance(seqx, seq4) != 6 {
		t.Errorf("Distance(seqx, seq4) = %d; want 6", got)
	}

	got = Distance(seqx, seq5)
	if Distance(seqx, seq5) != 12 {
		t.Errorf("Distance(seqx, seq5) = %d; want 12", got)
	}

	got = Distance(seqx, seq6)
	if Distance(seqx, seq6) != 17 {
		t.Errorf("Distance(seqx, seq6) = %d; want 17", got)
	}

	got = Distance(seqx, seq7)
	if Distance(seqx, seq7) != 24 {
		t.Errorf("Distance(seqx, seq7) = %d; want 24", got)
	}

	got = Distance(seqx, seq8)
	if Distance(seqx, seq8) != 3 {
		t.Errorf("Distance(seqx, seq8) = %d; want 3", got)
	}

	got1 := Distance(seqx, seq1)
	got2 := Distance(seq1, seqx)
	if got1 != got2 {
		t.Errorf("Symmetry mismatch in seq1: %d vs. %d", got1, got2)
	}

	got1 = Distance(seqx, seq2)
	got2 = Distance(seq2, seqx)
	if got1 != got2 {
		t.Errorf("Symmetry mismatch in seq2: %d vs. %d", got1, got2)
	}

	got1 = Distance(seqx, seq3)
	got2 = Distance(seq3, seqx)
	if got1 != got2 {
		t.Errorf("Symmetry mismatch in seq3: %d vs. %d", got1, got2)
	}

	got1 = Distance(seqx, seq4)
	got2 = Distance(seq4, seqx)
	if got1 != got2 {
		t.Errorf("Symmetry mismatch in seq4: %d vs. %d", got1, got2)
	}

	got1 = Distance(seqx, seq5)
	got2 = Distance(seq5, seqx)
	if got1 != got2 {
		t.Errorf("Symmetry mismatch in seq5: %d vs. %d", got1, got2)
	}

	got1 = Distance(seqx, seq6)
	got2 = Distance(seq6, seqx)
	if got1 != got2 {
		t.Errorf("Symmetry mismatch in seq6: %d vs. %d", got1, got2)
	}

	got1 = Distance(seqx, seq7)
	got2 = Distance(seq7, seqx)
	if got1 != got2 {
		t.Errorf("Symmetry mismatch in seq7: %d vs. %d", got1, got2)
	}

	got1 = Distance(seqx, seq8)
	got2 = Distance(seq8, seqx)
	if got1 != got2 {
		t.Errorf("Symmetry mismatch in seq8: %d vs. %d", got1, got2)
	}
}
