import React, { useEffect, useState } from "react";
import {
    Box,
    Button,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Stack,
    Text,
    useDisclosure
} from "@chakra-ui/react";

const ChatContext = React.createContext({
    messages: [], fetchMessages: () => {}
})

export default function ChatBody() {
    const [messages, setMessages] = useState([])
    const fetchMessages = async () => {
        const response = await fetch("http://127.0.0.1:8000/messages")
        const messages = await response.json()
        setMessages(messages.data)
    }

    useEffect(() => {
        fetchMessages()
    }, [])

    return (
        <ChatContext.Provider value={{messages, fetchMessages}}>
            <Stack spacing={5}>
                {messages.map((message) => (
                    <b>{message}</b>
                ))}
            </Stack>
        </ChatContext.Provider>
    )
}
