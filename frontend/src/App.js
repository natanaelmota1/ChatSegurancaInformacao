import logo from "./logo.svg";
import React, { useState, useEffect } from "react";
import "./App.css";
// import BigInt from 'big-integer'
// import Elgamal from 'elgamal'

const clientId = Math.floor(new Date().getTime() / 1000);

function gcd(a, b){
  if (a < b) return gcd(b, a)
  else if (a % b === 0) return b
  else return gcd(b, a % b)
}

function generateKey(q) {
  // const a = BigInt(Math.floor(Math.random() * q)); // Generate a random integer a in the range [2, p-2]
  var key = Math.floor(Math.random() * q  )// Generate a random integer a in the range [2, p-2]
  while (gcd(q, key) !== 1){
    key = Math.floor(Math.random() * q)
  }

  return key
  // const A = g * a % p; // Calculate the corresponding public key A
  // return { privateKey: a, publicKey: A };
}

function power(a, b, c){
  var x = 1
  var y = a

  while (b > 0){
    if (b % 2 !== 0){
      x = (x * y) % c
    }
    y = (y * y) % c
		b = (b / 2) >> 0
  }
	return x % c
}

function encryptMessage(message, q, h, g) {
  var encrypted = []
  const k = generateKey(q)
  const s = power(h, k, q) // Generate a random integer k in the range [2, p-2]
  const p = power(g, k, q)

  for (var i in message){
    encrypted.push(i)
  }

  for (var j in encrypted){
    j = s * j.codePointAt(0)
  }
  // const c1 = g * k % p; // Calculate the first component of the ciphertext
  // const c2 = (A * k * message) % p; // Calculate the second component of the ciphertext
  // return { c1: c1, c2: c2 };
  return { encrypted, p }
}

function decryptMessage(encrypted, p, key, q) {
  // const m = c1 * (p - 1 - a) % p; // Calculate the decrypted message
  // return m;
  var decrypted = ""
  var h = power(p, key, q)
  for (var i in encrypted) {
    decrypted = decrypted + String.fromCharCode(parseInt(i/h))
  }
  return decrypted
}

const q = Math.floor(Math.random() * 10**50)
const g = Math.floor(Math.random() * q)
const privateKey = Math.floor(Math.random() * (q-1))

const h = g ** privateKey % g
const publicKey = q.toString() + " " + h.toString() + " " + g.toString()

// const p = BigInt('2048'); // Choose a prime number
// const g = BigInt('2'); // Choose a primitive root of p
// const { privateKey, publicKey } = generateKey(p, g);
console.log('PrivateKey', privateKey)
console.log('PublicKey', publicKey)


function App() {
  // add random cliend id by date time
  

  // const [chatHistory, setChatHistory] = useState([])
  const [websckt, setWebsckt] = useState();
  const [message, setMessage] = useState([]);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const url = "ws://localhost:8000/ws/" + clientId;
    const ws = new WebSocket(url);

    ws.onopen = (event) => {
      const connectedMsg = 'Connected'
      const { encryption, p } = encryptMessage(connectedMsg, q, h, g)
      console.log('Welcome: ', encryption)
      const msgKey = {encryption, p, publicKey}
      console.log('msgKey', msgKey)
      ws.send(encryption);
      // ws.send(connectedMsg);

    };

    // recieve message every start page
    ws.onmessage = (e) => {
      const message = JSON.parse(e.data);
      console.log(message)
      const decryption = decryptMessage(message.message, message.p, privateKey);
      console.log('Decrypyted Message: ', decryption)
      setMessages([...messages, message]);
    };

    setWebsckt(ws);
    //clean up function when we close page
    return () => ws.close();
  }, []);

  const sendMessage = () => {
    const { encryption, p } = encryptMessage(message, q, h, g)
    console.log('Encrypted Message: ', encryption)
    const msgKey = {encryption, p, publicKey}
    console.log('msgKey', msgKey)
    websckt.send(encryption);
    // websckt.send(message);

    // recieve message every send message
    websckt.onmessage = (e) => {
      const message = JSON.parse(e.data);
      setMessages([...messages, message]);
    };
    setMessage([]);
  };

  return (
    <div className="container">
      <h1>Chat</h1>
      <h2>your client id: {clientId} </h2>
      <div className="chat-container">
        <div className="chat">
          {messages.map((value, index) => {
            if (value.clientId === clientId) {
              return (
                <div key={index} className="my-message-container">
                <div className="my-message">
                  <p className="client">client id : {clientId}</p>
                  <p className="message">{value.message}</p>
                </div>
              </div>
              );
            } else {
              return (
                <div key={index} className="another-message-container">
                  <div className="another-message">
                    <p className="client">client id : {clientId}</p>
                    <p className="message">{value.message}</p>
                  </div>
                </div>
              );
            }
          })}
        </div>
        <div className="input-chat-container">
        <input
            className="input-chat"
            type="text"
            placeholder="Chat message ..."
            onChange={(e) => setMessage(e.target.value)}
            value={message}
          ></input>
          <button type="submit" className="submit-chat" onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;