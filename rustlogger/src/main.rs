use std::net::TcpListener;
use std::net::SocketAddr;
use std::net::TcpStream;
use std::thread;
use std::io::{Read};

extern crate redis;
use redis::{Commands, RedisResult};

fn main() {
    start_server();
}

fn handle_client(mut stream: &TcpStream) {
    let mut s = String::new();
    stream.read_to_string(&mut s);
    println!("reading: {}", s);


}

pub fn start_server() {
    let listener = TcpListener::bind("0.0.0.0:27500").unwrap();

    println!("listener");
    for stream in listener.incoming() {
        println!("listener inside");

        match stream {
            Ok(stream) => {
                thread::spawn(move || {
                    // connection succeeded
                    handle_client(&stream)
                });
            }
            Err(e) => {
                println!("Connection failed !");
            }
        }
    }

    println!("Listening on 0.0.0.0:27500");
}




fn try_redis() -> redis::RedisResult<String> {
    let client = try!(redis::Client::open("redis://127.0.0.1/"));
    let con = try!(client.get_connection());
    try!(con.set("my_key", "<string>"));

    con.get("my_key")
}