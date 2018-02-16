pub enum Command {
    Cat,
    Echo,
    Lex,
    Print3,
    Shell,
}


use self::Command::*;


pub fn identify(all_args: &Vec<String>) -> (Command, Vec<String>) {
    match all_args.get(1) {
        Some(s) => {
            if      s == "echo" { (Echo, skip_2(all_args)) }
            else if s == "cat"  { (Cat,  skip_2(all_args)) }
            else if s == "lex"  { (Lex,  skip_2(all_args)) }
            else { (Print3, skip_2(all_args)) }
        },
        None => (Shell, Vec::new()),
    }
}


fn skip_2(all_args: &Vec<String>) -> Vec<String> {
    Vec::from(&all_args[2..])
}
