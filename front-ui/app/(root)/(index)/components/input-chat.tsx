import React, { useState } from 'react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import chatAction from '@/lib/actions/chat-action';

interface InputChatProps {
    currentMessage: string;
    onChangeMessage: (e: string[]) => void;
}

const InputChat = ({ currentMessage, onChangeMessage }: InputChatProps) => {
    const [value, setValue] = useState<string>('');
    return (
        <section className="container mx-auto flex gap-2 my-2">
            <Input
                type="text"
                placeholder="Type your message here."
                className="rounded-lg"
                onChange={(e) => {                    
                    setValue(e.target.value);
                }}
            />
            <Button onClick={() => {
                onChangeMessage([...currentMessage, value]);
                chatAction({ 
                    prompt: value, 
                    // context: currentMessage.join('\n') 
                });
                setValue('');
            }}>
                Send
            </Button>
        </section>
    );
};

export default InputChat;