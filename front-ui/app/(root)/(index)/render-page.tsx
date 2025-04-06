'use client';

import React, { useState } from 'react';

import InputChat from './components/input-chat';
import ShowChat from './components/show-chat';

const RenderPage = () => {
    const [messages, setMessages] = useState<string[]>([]);
    const [result, setResult] = useState<string[]>([]);

    console.log(messages);

    return (
        <main className="py-10">
            <ShowChat>
                <p>Hello</p>
            </ShowChat>
            <InputChat 
                currentMessage={messages}
                onChange={setMessages}
            />
        </main>
    );
};

export default RenderPage;