import logo from "./logo.svg";
import React, { useState, useEffect } from "react";
import "./App.css";
import BigInt from 'big-integer'

const clientId = Math.floor(new Date().getTime() / 1000);

// function gcd(a, b) {
//   console.log('entrou aqui', a, b)
//   if (a < b) {
//     return gcd(b, a);
//   } else if (a % b === 0) {
//     return b;
//   } else {
//     return gcd(b, a % b);
//   }
// }

function generateKey(q) {
  let key = BigInt(Math.floor(Math.random() * (q - 2 * BigInt(10 ** 20))) + BigInt(10 ** 20));
  console.log('key', key)
  // while (gcd(q, key) !== 1) {
  //   key = BigInt(Math.floor(Math.random() * (q - 2 * BigInt(10 ** 20))) + BigInt(10 ** 20));
  // }
  return key;
}

function power(a, b, c) {
  let x = 1;
  let y = a;

  while (b > 0) {
    if (b % 2 !== 0) {
      x = (x * y) % c;
    }
    y = (y * y) % c;
    b = Math.floor(b / 2);
  }

  return BigInt(Math.floor(x % c));
}

function encryptMessage(msg, q, h, g) {
  const en_msg = [];
  const k = generateKey(q); // Private key for sender
  const s = power(h, k, q);
  const p = power(g, k, q);

  for (let i = 0; i < msg.length; i++) {
    en_msg.push(msg.charCodeAt(i));
  }

  for (let i = 0; i < en_msg.length; i++) {
    en_msg[i] = s * en_msg[i];
  }

  return [en_msg, p];
}

function decryptMessage(en_msg, p, key, q) {
  let dr_msg = '';
  const h = power(p, key, q);

  for (let i = 0; i < en_msg.length; i++) {
    dr_msg += String.fromCharCode(Math.floor(en_msg[i] / h));
  }

  return dr_msg;
}

const q = BigInt(Math.floor(Math.random() * (BigInt(10 ** 50) - BigInt(10 ** 20))) + BigInt(10 ** 20));
const g = BigInt(Math.floor(Math.random() * (q - 2)) + 2);
const privateKey = BigInt(Math.floor(Math.random() * (q - 2)) + 2);
const h = BigInt(power(g, privateKey, q));

const publicKey = `${q} ${h} ${g}`;

// const p = BigInt('2048'); // Choose a prime number
// const g = BigInt('2'); // Choose a primitive root of p
// const { privateKey, publicKey } = generateKey(p, g);
console.log('PrivateKey', privateKey)
console.log('PublicKey', publicKey)

function encrypt(message, ws){
  const encryption = encryptMessage(message, q, h, g)

  for (let i = 0; i < encryption[0].length; i++){
    encryption[0][i] = BigInt(encryption[0][i])
  }

  const msgJson = {
    sender: clientId,
    message: encryption[0],
    p: BigInt(encryption[1]),
    key: publicKey
  }
  console.log('msgKey', msgJson)
  ws.send(JSON.stringify(msgJson));
}

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
      // ws.send(connectedMsg);

      encrypt(connectedMsg, ws)

    };

    // recieve message every start page
    ws.onmessage = (e) => {
      const message = JSON.parse(e.data);

      const decryption = decryptMessage(
        message.message,
        message.p,
        privateKey,
        q
      );

      console.log('Decrypyted Message: ', decryption)

      setMessages([...messages, decryption]);
    };

    setWebsckt(ws);
    //clean up function when we close page
    return () => ws.close();
  }, []);

  const sendMessage = () => {
    encrypt(message, websckt)

    // websckt.send(message);

    // recieve message every send message
    websckt.onmessage = (e) => {
      const message = JSON.parse(e.data);
      const decryption = decryptMessage(
        message.message,
        message.p,
        privateKey,
        q
      );
      setMessages([...messages, decryption]);
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