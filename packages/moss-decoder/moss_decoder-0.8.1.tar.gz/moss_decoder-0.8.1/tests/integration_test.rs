use crate::moss_protocol::test_util::*;
use moss_decoder::*;

use pretty_assertions::assert_eq;

const FILE_MOSS_NOISE: &str = "tests/test-data/moss_noise.raw";
const FILE_4_EVENTS_PARTIAL_END: &str = "tests/test-data/moss_noise_0-499b.raw"; // 4 events, last event is partial ~4.5 events
const FILE_3_EVENTS_PARTIAL_START: &str = "tests/test-data/moss_noise_500-999b.raw"; // 3 events, first event is partial ~3.5 events
const FILE_MOSS_NOISE_ALL_REGION: &str = "tests/test-data/noise_all_regions.raw";
const FILE_NOISE_RANDOM_REGION: &str = "tests/test-data/noise_random_region.raw";
const FILE_PATTERN_ALL_REGIONS: &str = "tests/test-data/pattern_all_regions.raw";

#[test]
fn test_decoding_single_event() {
    //
    let event = fake_event_simple();

    let (packet, last_trailer_idx) = decode_event(&event).unwrap();

    assert!(
        last_trailer_idx == event.len() - 1,
        "All bytes were not processed!"
    );

    assert_eq!(
        packet,
        MossPacket {
            unit_id: 1,
            hits: vec![
                MossHit {
                    region: 0,
                    row: 2,
                    column: 8
                },
                MossHit {
                    region: 0,
                    row: 10,
                    column: 8
                },
                MossHit {
                    region: 1,
                    row: 301,
                    column: 433
                },
                MossHit {
                    region: 3,
                    row: 2,
                    column: 8
                },
            ]
        },
        "unexpected decoding result"
    );
}

#[test]
fn test_decoding_single_event_fsm() {
    //
    let event = fake_event_simple();

    let (packet, last_trailer_idx) = decode_event(&event).unwrap();

    assert!(
        last_trailer_idx == event.len() - 1,
        "All bytes were not processed!"
    );

    assert_eq!(
        packet,
        MossPacket {
            unit_id: 1,
            hits: vec![
                MossHit {
                    region: 0,
                    row: 2,
                    column: 8
                },
                MossHit {
                    region: 0,
                    row: 10,
                    column: 8
                },
                MossHit {
                    region: 1,
                    row: 301,
                    column: 433
                },
                MossHit {
                    region: 3,
                    row: 2,
                    column: 8
                },
            ]
        },
        "unexpected decoding result"
    );
}

#[test]
fn test_decoding_multiple_events_one_call() {
    let events = fake_multiple_events();

    let mut moss_packets: Vec<MossPacket> = Vec::new();

    // There's multiple events in the data but we only call decode_event once so we should only get one packet
    if let Ok((packet, _unprocessed_data)) = decode_event(&events) {
        moss_packets.push(packet);
    }

    let packet_count = moss_packets.len();

    for p in moss_packets {
        println!("{p:?}");
    }

    assert_eq!(packet_count, 1, "Expected 1 packet, got {}", packet_count);
}

#[test]
fn test_read_file_decode() {
    let time = std::time::Instant::now();

    println!("Reading file...");
    let f = std::fs::read(std::path::PathBuf::from(FILE_MOSS_NOISE)).unwrap();
    println!(
        "Read file in: {t:?}. Bytes: {cnt}",
        t = time.elapsed(),
        cnt = f.len()
    );

    println!("Decoding content...");
    let (p, last_trailer_idx) = decode_all_events(&f).unwrap();
    println!("Decoded in: {t:?}\n", t = time.elapsed());

    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");

    assert_eq!(
        last_trailer_idx,
        f.len() - 2,
        "All bytes were not processed!"
    );
    assert_eq!(p.len(), 100000, "Expected 100k packets, got {}", p.len());

    println!("{:#X?}", f.get(..=50));
}

#[test]
fn test_decode_from_file() {
    let time = std::time::Instant::now();
    let expect_packets = 100000;
    let expect_hits = 2716940;

    let packets = moss_decoder::decode_from_file(FILE_MOSS_NOISE.to_string().into()).unwrap();
    println!("Decoded in: {t:?}\n", t = time.elapsed());

    println!("Got: {packets}", packets = packets.len());

    assert_eq!(
        packets.len(),
        expect_packets,
        "Expected {expect_packets} packets, got {}",
        packets.len()
    );

    // Count total hits
    let total_hits = packets.iter().fold(0, |acc, p| acc + p.hits.len());
    assert_eq!(
        total_hits, expect_hits,
        "Expected {expect_hits} hits, got {total_hits}",
    );
}

#[test]
fn test_decode_from_file_noise_all_region() {
    let expect_packets = 1000;
    let expect_hits = 6085;

    let packets =
        moss_decoder::decode_from_file(FILE_MOSS_NOISE_ALL_REGION.to_string().into()).unwrap();
    assert_eq!(
        packets.len(),
        expect_packets,
        "Expected {expect_packets} packets, got {}",
        packets.len()
    );
    // Count total hits
    let total_hits = packets.iter().fold(0, |acc, p| acc + p.hits.len());
    assert_eq!(
        total_hits, expect_hits,
        "Expected {expect_hits} hits, got {total_hits}",
    );
}

#[test]
fn test_decode_from_file_noise_random_region() {
    let expect_packets = 1044;
    let expect_hits = 5380;

    let packets =
        moss_decoder::decode_from_file(FILE_NOISE_RANDOM_REGION.to_string().into()).unwrap();
    assert_eq!(
        packets.len(),
        expect_packets,
        "Expected {expect_packets} packets, got {}",
        packets.len()
    );
    // Count total hits
    let total_hits = packets.iter().fold(0, |acc, p| acc + p.hits.len());
    assert_eq!(
        total_hits, expect_hits,
        "Expected {expect_hits} hits, got {total_hits}",
    );
}

#[test]
fn test_decode_from_file_pattern_all_region() {
    let expect_packets = 1000;
    let expect_hits = 4000;

    let packets =
        moss_decoder::decode_from_file(FILE_PATTERN_ALL_REGIONS.to_string().into()).unwrap();
    assert_eq!(
        packets.len(),
        expect_packets,
        "Expected {expect_packets} packets, got {}",
        packets.len()
    );
    // Count total hits
    let total_hits = packets.iter().fold(0, |acc, p| acc + p.hits.len());
    assert_eq!(
        total_hits, expect_hits,
        "Expected {expect_hits} hits, got {total_hits}",
    );
}

#[test]
fn test_decode_protocol_error() {
    pyo3::prepare_freethreaded_python();

    let event = fake_event_protocol_error();

    match decode_event(&event) {
        Ok(_) => {
            panic!("This packet has a protocol error, but it was not detected!")
        }
        Err(e) if e.to_string().contains("Decoding failed") => {
            println!("Got expected error: {e}");
        }
        Err(e) => {
            panic!("Got unexpected error: {e}");
        }
    }
}

#[test]
fn test_decode_multiple_events_fsm() {
    let expect_packets = 100000;
    let expect_hits = 2716940;

    println!("Reading file...");
    let time = std::time::Instant::now();

    let f = std::fs::read(std::path::PathBuf::from(FILE_MOSS_NOISE)).unwrap();
    println!(
        "Read file in: {t:?}. Bytes: {cnt}",
        t = time.elapsed(),
        cnt = f.len()
    );

    println!("Decoding content...");
    let (p, last_trailer_idx) = decode_all_events(&f).unwrap();
    println!("Decoded in: {t:?}\n", t = time.elapsed());

    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");
    println!("Last 10 bytes of file: {:X?}", f.get(f.len() - 10..));

    assert_eq!(
        last_trailer_idx,
        f.len() - 2,
        "All bytes were not processed!"
    );
    assert_eq!(
        p.len(),
        expect_packets,
        "Expected 100k packets, got {}",
        p.len()
    );

    // Count total hits
    let total_hits = p.iter().fold(0, |acc, p| acc + p.hits.len());
    assert_eq!(
        total_hits, expect_hits,
        "Expected {expect_hits} hits, got {total_hits}",
    );
}

#[test]
fn test_decode_from_file_fsm() {
    let time = std::time::Instant::now();
    let expect_packets = 100000;
    let expect_hits = 2716940;

    let packets = moss_decoder::decode_from_file(FILE_MOSS_NOISE.to_string().into()).unwrap();
    println!("Decoded in: {t:?}\n", t = time.elapsed());

    println!("Got: {packets}", packets = packets.len());

    assert_eq!(
        packets.len(),
        expect_packets,
        "Expected {expect_packets} packets, got {}",
        packets.len()
    );

    // Count total hits
    let total_hits = packets.iter().fold(0, |acc, p| acc + p.hits.len());
    assert_eq!(
        total_hits, expect_hits,
        "Expected {expect_hits} hits, got {total_hits}",
    );
}

#[test]
fn test_decode_protocol_error_fsm() {
    pyo3::prepare_freethreaded_python();

    let event = fake_event_protocol_error();

    match decode_event(&event) {
        Ok(_) => {
            panic!("This packet has a protocol error, but it was not detected!")
        }
        Err(e) if e.to_string().contains("Decoding failed") => {
            println!("Got expected error: {e}");
        }
        Err(e) => {
            panic!("Got unexpected error: {e}");
        }
    }
}

#[test]
fn test_decode_events_skip_0_take_10() {
    let take = 10;
    let f = std::fs::read(std::path::PathBuf::from(FILE_MOSS_NOISE)).unwrap();
    let (p, last_trailer_idx) = decode_n_events(&f, take, None, None).unwrap();

    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");
    assert_eq!(p.len(), take, "Expected {take} packets, got {}", p.len());
}

#[test]
fn test_decode_events_skip_10_take_1() {
    let skip = 10;
    let take = 1;
    let f = std::fs::read(std::path::PathBuf::from(FILE_MOSS_NOISE)).unwrap();

    let (p, last_trailer_idx) = decode_n_events(&f, take, Some(skip), None).unwrap();

    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");
    assert_eq!(p.len(), take, "Expected {take} packets, got {}", p.len());
}

#[test]
fn test_decode_events_skip_500_take_100() {
    let skip = 500;
    let take = 100;
    let f = std::fs::read(std::path::PathBuf::from(FILE_MOSS_NOISE)).unwrap();

    let (p, last_trailer_idx) = decode_n_events(&f, take, Some(skip), None).unwrap();

    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");
    assert_eq!(p.len(), take, "Expected {take} packets, got {}", p.len());
}

#[test]
fn test_decode_events_skip_99000_take_1000() {
    let skip = 99000;
    let take = 1000;
    let f = std::fs::read(std::path::PathBuf::from(FILE_MOSS_NOISE)).unwrap();

    let (p, last_trailer_idx) = decode_n_events(&f, take, Some(skip), None).unwrap();
    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");
    assert_eq!(p.len(), take, "Expected {take} packets, got {}", p.len());
}

#[test]
#[should_panic = "Failed decoding packet #5"]
fn test_decode_split_events_skip_0_take_5() {
    pyo3::prepare_freethreaded_python();
    let take = 5;
    let f = std::fs::read(std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END)).unwrap();

    let (p, last_trailer_idx) = decode_n_events(&f, take, None, None).unwrap();

    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");
    assert_eq!(p.len(), take, "Expected {take} packets, got {}", p.len());
}

#[test]
fn test_decode_split_events_skip_1_take_2() {
    pyo3::prepare_freethreaded_python();
    let skip = 1;
    let take = 2;
    let f = std::fs::read(std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END)).unwrap();

    let (p, last_trailer_idx) = decode_n_events(&f, take, Some(skip), None).unwrap();

    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");
    assert_eq!(p.len(), take, "Expected {take} packets, got {}", p.len());
}

#[test]
fn test_decode_split_events_from_partial_event_skip_1_take_2() {
    pyo3::prepare_freethreaded_python();
    let skip = 1;
    let take = 2;
    let f = std::fs::read(std::path::PathBuf::from(FILE_3_EVENTS_PARTIAL_START)).unwrap();

    let (p, last_trailer_idx) = decode_n_events(&f, take, Some(skip), None).unwrap();

    println!("Got: {packets} packets", packets = p.len());
    println!("Last trailer at index: {last_trailer_idx}");
    assert_eq!(p.len(), take, "Expected {take} packets, got {}", p.len());
}

#[test]
fn test_decode_split_events_with_remainder() {
    pyo3::prepare_freethreaded_python();
    let take = 100;
    let f = std::fs::read(std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END)).unwrap();

    assert!(decode_n_events(&f, take, None, None).is_err());

    let (packets, remainder) = skip_n_take_all(&f, 0).unwrap();

    let remainder = remainder.unwrap();
    let packets = packets.unwrap();

    println!("Got: {packets} packets", packets = packets.len());
    println!("Remainder: {remainder} bytes", remainder = remainder.len());
    assert_eq!(packets.len(), 4);
    assert_eq!(remainder.len(), 43);
}

#[test]
fn test_decode_split_events_from_both_files() {
    pyo3::prepare_freethreaded_python();
    let take = 6;
    let f = std::fs::read(std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END)).unwrap();
    let f2 = std::fs::read(std::path::PathBuf::from(FILE_3_EVENTS_PARTIAL_START)).unwrap();

    // First attempt to decode 6 events from the first file, that should fail
    assert!(decode_n_events(&f, take, None, None).is_err());

    // Then fall back to decoding as many as possible and returning the remainder
    let (packets, remainder) = skip_n_take_all(&f, 0).unwrap();
    let packets = packets.unwrap();
    let decoded_packets = packets.len();

    // Now take the rest from the remainder and the next file
    let (packets2, last_trailer_idx) =
        decode_n_events(&f2, take - decoded_packets, None, remainder).unwrap();

    println!("Got: {packets} packets", packets = packets.len());
    println!("Got: {packets2} packets", packets2 = packets2.len());
    println!("Last trailer at index: {last_trailer_idx}");
    assert_eq!(packets.len() + packets2.len(), take);
}

#[test]
fn test_decode_2_events_from_path() {
    pyo3::prepare_freethreaded_python();
    let take = 2;
    let p = std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END);
    let res = decode_n_events_from_file(p, take, None, None);
    let packets = res.unwrap();
    println!("Got: {packets} packets", packets = packets.len());
    assert_eq!(packets.len(), take);
}

#[test]
fn test_decode_split_events_from_path_repeated_until_err() {
    pyo3::prepare_freethreaded_python();
    let take_first = 2;
    let p = std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END);
    let res = decode_n_events_from_file(p.clone(), take_first, None, None);
    let mut running_packets = res.unwrap();
    println!("Got: {packets} packets", packets = running_packets.len());
    assert_eq!(running_packets.len(), take_first);

    let take_second = 2;
    let res = decode_n_events_from_file(p.clone(), take_second, Some(running_packets.len()), None);
    running_packets.extend(res.unwrap());
    println!("Got: {packets} packets", packets = running_packets.len());
    assert_eq!(running_packets.len(), take_first + take_second);

    let take_third = 2;
    let res = decode_n_events_from_file(p, take_third, Some(running_packets.len()), None);
    println!("Got : {:?}", res);
    assert!(res.is_err());
    assert!(res
        .unwrap_err()
        .to_string()
        .contains("No MOSS Packets in events"));
}

#[test]
fn test_decode_split_events_from_path_take_too_many() {
    pyo3::prepare_freethreaded_python();
    let take_first = 10;
    let p = std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END);
    let res = decode_n_events_from_file(p.clone(), take_first, None, None);
    println!("Got : {:?}", res);
    assert!(res.is_err());
    assert!(res.unwrap_err().to_string().contains("BytesWarning"));
}

#[test]
fn test_skip_n_take_all_from_file() {
    pyo3::prepare_freethreaded_python();
    let p = std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END);
    let res = skip_n_take_all_from_file(p.clone(), 0);
    assert!(res.is_ok());
    let (packets, remainder) = res.unwrap();
    assert!(packets.is_some());
    assert!(remainder.is_some());
    assert_eq!(packets.unwrap().len(), 4);
    let remainder = remainder.unwrap();
    println!("Got {} remainder bytes", remainder.len());
    println!("Got remainder: {:02X?}", remainder);

    let (packets, _) = skip_n_take_all_from_file(p.clone(), 1).unwrap();
    assert_eq!(packets.unwrap().len(), 3);
    let (packets, _) = skip_n_take_all_from_file(p.clone(), 2).unwrap();
    assert_eq!(packets.unwrap().len(), 2);
    let (packets, _) = skip_n_take_all_from_file(p.clone(), 3).unwrap();
    assert_eq!(packets.unwrap().len(), 1);
    let (packets, _) = skip_n_take_all_from_file(p.clone(), 4).unwrap();
    assert!(packets.is_none());
}

#[test]
fn test_decode_split_events_from_file_spillover() {
    pyo3::prepare_freethreaded_python();
    let mut running_packets = Vec::new();
    let take = 2;
    let p = std::path::PathBuf::from(FILE_4_EVENTS_PARTIAL_END);
    loop {
        let skip = if running_packets.is_empty() {
            None
        } else {
            Some(running_packets.len())
        };
        let res = decode_n_events_from_file(p.clone(), take, skip, None);
        if res.is_err() {
            println!("Got error: {:?}", res);
            break;
        }
        running_packets.extend(res.unwrap());
    }
    let skip = running_packets.len();
    let (packets, remainder) = skip_n_take_all_from_file(p.clone(), skip).unwrap();
    assert!(
        packets.is_none(),
        "take is two ({take}) but there's still packets in the file"
    );
    let p2 = std::path::PathBuf::from(FILE_3_EVENTS_PARTIAL_START);
    let res = decode_n_events_from_file(p2.clone(), take, None, remainder);
    assert_eq!(res.unwrap().len(), 2);
}
