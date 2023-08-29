use pyo3::prelude::*;
use std::fs;

#[pyfunction]
fn p001_counting_dna_nucleotides(f_path: String) -> PyResult<String> {

    let dna = fs::read_to_string(f_path)
        .expect("Error: should have been able to read the file");

    let mut a_counts = 0;
    let mut c_counts = 0;
    let mut g_counts = 0;
    let mut t_counts = 0;

    for base in dna.chars() {
        match base {
            'A' => a_counts += 1,
            'C' => c_counts += 1,
            'G' => g_counts += 1,
            'T' => t_counts += 1,
            _ => (),
        }
    }

    let count_str = format!("{} {} {} {}", a_counts, c_counts, g_counts, t_counts);
    return Ok(count_str);
}

#[pyfunction]
fn p002_transcribing_dna_into_rna(f_path: String) -> PyResult<String> {

    let dna = fs::read_to_string(f_path)
        .expect("Error: should have been able to read the file");

    let mut rna = String::from("");

    for base in dna.chars() {
        match base {
            'T' => rna.push('U'),
            other => rna.push(other),
        }
    }

    return Ok(rna);
}

#[pyfunction]
fn p003_complementing_a_strand_of_dna(f_path: String) -> PyResult<String> {

    let dna = fs::read_to_string(f_path)
        .expect("Error: should have been able to read the file");

    let mut rev_comp = String::from("");

    for base in dna.chars().rev() {
        match base {
            'A' => rev_comp.push('T'),
            'C' => rev_comp.push('G'),
            'G' => rev_comp.push('C'),
            'T' => rev_comp.push('A'),
            _ => (),
        }
    }

    return Ok(rev_comp);
}

#[pymodule]
fn rosalind(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(p001_counting_dna_nucleotides, m)?)?;
    m.add_function(wrap_pyfunction!(p002_transcribing_dna_into_rna, m)?)?;
    m.add_function(wrap_pyfunction!(p003_complementing_a_strand_of_dna, m)?)?;
    Ok(())
}
