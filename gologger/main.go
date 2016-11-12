package main

import (
    "os"
    "net"
    "fmt"
    "regexp"
    "strings"
    "github.com/adjust/redismq"
)

const (
    CONN_PORT = "27500"
    CONN_TYPE = "tcp"
    BOT_RE = `^".*?<\d+><BOT><.*?>"`
)

var reBot, _ = regexp.Compile(BOT_RE)

func main() {
    ln, err := net.Listen(CONN_TYPE, ":" + CONN_PORT)

    q := redismq.CreateQueue("localhost", "6379", "", 0, "ndstats")

    if err != nil {
        fmt.Println("cant bind socket")
        os.Exit(1)
    }

    // Close the listener when the application closes.
    defer ln.Close()
    fmt.Println("Listening on :" + CONN_PORT)

    for {
	    conn, err := ln.Accept()
        if err != nil {
            // handle error
        } else {
            go handleLine(q, conn)
        }
    }
}

func handleLine(q *redismq.Queue, conn net.Conn) {
    defer conn.Close()
    buf := make([]byte, 1024)

    msgLen, err := conn.Read(buf)
    if err != nil {
        fmt.Println("Error reading:", err.Error())
        return
    }

    msgString := string(buf[0:msgLen])

    botMatch := reBot.MatchString(msgString)
    if (botMatch) {
        return
    }

    fullAddr := conn.RemoteAddr().String()
    addrIdx := strings.LastIndex(fullAddr, ":")
    addr := fullAddr[0:addrIdx]

    finalMsg := addr + "|" + msgString

    fmt.Println("formatted message: ", finalMsg)

    q.Put(finalMsg)
    // redismq::ndstats

}