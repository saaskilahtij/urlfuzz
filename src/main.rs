use std::env;
use regex::Regex;
use url::{Url};

fn main() {
    let args: Vec<String> = env::args().collect();
    let re = Regex::new(r"^(https|http|ftp):\/\/(www\.)?(([a-zA-Z0-9]*\.)*)[a-z]{2,63}((\/[a-zA-Z0-9]*)*)?(\?[a-zA-Z0-9]*=?([a-zA-Z0-9]*)?)?(\&[a-zA-Z0-9]*=?[a-zA-Z0-9]*)*(#[a-zA-Z0-9]*)?$").unwrap();
    if args.len() < 2 {
        eprintln!("Usage: url_validator <URL>");
        std::process::exit(1);
    }

    let url = &args[1];
    let a: *const i32 = std::ptr::null();

    if re.is_match(url) && !is_valid(url) {
        unsafe {
            println!("{}", *a);
        }
    } else if !re.is_match(url) && is_valid(url){
        unsafe {
            println!("{}", *a)
        }
    }
}


fn is_valid(url: &str) -> bool {
    Url::parse(url).is_ok()
}
