import React from "react";
import { render } from 'react-dom';
import { ChakraProvider } from "@chakra-ui/react";

import Header from "./components/Header";
import ChatBody from "./components/ChatBody";
function App() {
  return (
    <ChakraProvider>
      <Header />
      <ChatBody />
    </ChakraProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)