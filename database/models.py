from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Dataset(Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    resolver = Column(String, nullable=False)
    dns_type = Column(String, nullable=False)
    padding = Column(String)
    caching = Column(String, nullable=False)
    hostname = Column(String, nullable=False)
    ips = Column(ARRAY(String), nullable=False)
    world = Column(String)
    app = relationship("App", cascade="save-update, merge, delete")

    def __init__(self, name, resolver, dns_type, padding, caching, hostname, ips, world):
        self.name = name
        self.resolver = resolver
        self.dns_type = dns_type
        self.padding = padding
        self.caching = caching
        self.hostname = hostname
        self.ips = ips
        self.world = world

    def __repr__(self):
        return '<dataset(id={}, name={}, resolver={}, dns_type={}, padding={}, caching={}, hostname={}, ips={})>'.format(
            self.id, self.name, self.resolver, self.dns_type, self.padding, self.caching, self.hostname, self.ips)


class App(Base):
    __tablename__ = 'app'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dataset_id = Column(Integer, ForeignKey('dataset.id'))
    trace = relationship("Trace", cascade="save-update, merge, delete")

    def __init__(self, name, dataset_id):
        self.name = name
        self.dataset_id = dataset_id

    def __repr__(self):
        return "<app(id={}, name='{}', dataset_id={})>".format(self.id, self.name, self.dataset_id)


class Trace(Base):
    __tablename__ = 'trace'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    app_id = Column(Integer, ForeignKey('app.id'))
    features = relationship("Features", cascade="save-update, merge, delete")
    packet = relationship("Packet", cascade="save-update, merge, delete")

    def __init__(self, timestamp, app_id):
        self.timestamp = timestamp
        self.app_id = app_id

    def __repr__(self):
        return "<trace(id={}, timestamp={}, app_id={})>".format(self.id, self.timestamp, self.app_id)


class Features(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    trace_id = Column(Integer, ForeignKey('trace.id'))
    datetime_trace = Column(DateTime)
    app_name = Column(String)
    # nr of packets
    nr_dns_packets = Column(Integer)
    nr_dns_req = Column(Integer)
    nr_dns_resp = Column(Integer)
    # tls record sizes
    tls_sizes = Column(ARRAY(Integer))
    tls_sizes_req = Column(ARRAY(Integer))
    tls_sizes_resp = Column(ARRAY(Integer))
    # mean of sizes
    mean_tls_sizes = Column(Float)
    mean_responses_tls_sizes = Column(Float)
    mean_requests_tls_sizes = Column(Float)
    # sd of sizes
    sd_tls_sizes = Column(Float)
    sd_requests_tls_sizes = Column(Float)
    sd_responses_tls_sizes = Column(Float)
    # median of sizes
    median_tls_sizes = Column(Float)
    median_requests_tls_sizes = Column(Float)
    median_responses_tls_sizes = Column(Float)
    # time to previous packet in seconds
    tls_sizes_times = Column(ARRAY(String))
    # nr of occurence of multiple tls records in one trace
    mult_tls_records = Column(Integer)

    def __init__(self, trace_id, datetime_trace, app_name,
                 nr_dns_packets, nr_dns_req, nr_dns_resp,
                 tls_sizes, tls_sizes_req, tls_sizes_resp,
                 mean_tls_sizes, mean_requests, mean_responses,
                 sd_tls_sizes, sd_requests, sd_respones,
                 median_tls_sizes, median_requests, median_responses,
                 tls_sizes_times, mult_tls_records):
        self.trace_id = trace_id
        self.datetime_trace = datetime_trace
        self.app_name = app_name
        self.nr_dns_packets = nr_dns_packets
        self.nr_dns_req = nr_dns_req
        self.nr_dns_resp = nr_dns_resp
        self.tls_sizes = tls_sizes
        self.tls_sizes_req = tls_sizes_req
        self.tls_sizes_resp = tls_sizes_resp
        self.mean_tls_sizes = mean_tls_sizes
        self.mean_requests_tls_sizes = mean_requests
        self.mean_responses_tls_sizes = mean_responses
        self.sd_tls_sizes = sd_tls_sizes
        self.sd_requests_tls_sizes = sd_requests
        self.sd_responses_tls_sizes = sd_respones
        self.median_tls_sizes = median_tls_sizes
        self.median_requests_tls_sizes = median_requests
        self.median_responses_tls_sizes = median_responses
        self.tls_sizes_times = tls_sizes_times
        self.mult_tls_records = mult_tls_records

    def __repr__(self):
        return "<feature(id={}, trace_id={}, time={], app_name={}, " \
               "nr_dns_pkts={}, nr_dns_pkts_req={},nr_dns_pkts_resp={}, " \
               "tls_sizes={}, tls_sizes_req={}, tls_sizes_resp={}, mean_tls_sizes={},mean_tls_sizes_req={}, " \
               "mean_tls_sizes_resp={}, sd_tls_sizes={}, sd_tls_sizes_req={},sd_tls_sizes_resp={},median_tls_sizes={" \
               "}, median_tls_sizes_req={}, median_tls_sizes_resp={}, times_tls_sizes={}, " \
               "mult_tls_records{})>".format(
            self.id, self.trace_id, self.datetime_trace, self.app_name,
            self.nr_dns_packets, self.nr_dns_req, self.nr_dns_resp,
            self.tls_sizes, self.tls_sizes_req, self.tls_sizes_resp, self.mean_tls_sizes,
            self.mean_requests_tls_sizes,
            self.mean_responses_tls_sizes, self.sd_tls_sizes, self.sd_requests_tls_sizes,
            self.sd_responses_tls_sizes,
            self.median_tls_sizes, self.median_requests_tls_sizes, self.median_responses_tls_sizes,
            self.tls_sizes_times, self.mult_tls_records)


class Packet(Base):
    __tablename__ = 'packet'
    id = Column(Integer, primary_key=True)
    trace_id = Column(Integer, ForeignKey('trace.id'))
    packet_nr = Column(Integer)
    packet_length = Column(Integer)
    tls_record_length = Column(Integer)
    direction = Column(String)
    mult_tls_records = Column(ARRAY(Integer))
    relative_time = Column(Float)

    def __init__(self, trace_id, packet_nr, packet_length, tls_record_length, direction, mult_tls_records,
                 relative_time):
        self.trace_id = trace_id
        self.packet_nr = packet_nr
        self.packet_length = packet_length
        self.tls_record_length = tls_record_length
        self.direction = direction
        self.mult_tls_records = mult_tls_records
        self.relative_time = relative_time

    def __repr__(self):
        return "<packet(id={}, packet_nr={}, packet_length={}, tls_record_length={}, direction='{}', time={}, " \
               "trace_id={}, mult_tls_records={})>".format(self.id, self.packet_nr, self.packet_length,
                                                           self.tls_record_length, self.direction,
                                                           self.relative_time,
                                                           self.trace_id, self.mult_tls_records)
