pub fn is_space(c: char) -> bool {
    match c {
        ' ' => true,
        '\n' => true,
        '\r' => true,
        '\t' => true,
        _ => false,
    }
}
