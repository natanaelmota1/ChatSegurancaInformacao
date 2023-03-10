import logo from "./logo.svg";
import React, { useState, useEffect } from "react";
import "./App.css";
import BigInt from 'big-integer'

const clientId = Math.floor(new Date().getTime() / 1000);

// function generateKeyPair(p, g) {
//   const a = BigInt(Math.floor(Math.random() * (p - 2n) + 2n)); // Generate a random integer a in the range [2, p-2]
//   const A = g ** a % p; // Calculate the corresponding public key A
//   return { privateKey: a, publicKey: A };
// }

// function encryptMessage(message, p, g, A) {
//   const k = BigInt(Math.floor(Math.random() * (p - 2n) + 2n)); // Generate a random integer k in the range [2, p-2]
//   const c1 = g ** k % p; // Calculate the first component of the ciphertext
//   const c2 = (A ** k * message) % p; // Calculate the second component of the ciphertext
//   return { c1: c1, c2: c2 };
// }

// function decryptMessage(c1, c2, a, p) {
//   const m = c2 * c1 ** (p - 1n - a) % p; // Calculate the decrypted message
//   return m;
// }

// const p = BigInt('1048583'); // Choose a prime number
// const g = BigInt('2'); // Choose a primitive root of p
// const { privateKey, publicKey } = generateKeyPair(p, g);
// console.log('PrivateKey: ', privateKey)
// console.log('PublicKey: ', publicKey)

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
      // const encryption = encryptMessage(connectedMsg, p, g, publicKey)
      // console.log('Welcome: ', encryption)
      // const msgKey = {encryption, p, publicKey}
      // console.log('msgKey', msgKey)
      // websckt.send(encryption);
      websckt.send(connectedMsg);

    };

    // recieve message every start page
    ws.onmessage = (e) => {
      const message = JSON.parse(e.data);
      // console.log(message)
      // const decryption = decryptMessage(message.c1, message.c2, privateKey, p);
      // console.log('Decrypyted Message: ', decryption)
      setMessages([...messages, message]);
    };

    setWebsckt(ws);
    //clean up function when we close page
    return () => ws.close();
  }, []);

  const sendMessage = () => {
    // const encryption = encryptMessage(message, p, g, publicKey)
    // console.log('Encrypted Message: ', encryption)
    // const msgKey = {encryption, p, publicKey}
    // console.log('msgKey', msgKey)
    // websckt.send(encryption);
    websckt.send(message);

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