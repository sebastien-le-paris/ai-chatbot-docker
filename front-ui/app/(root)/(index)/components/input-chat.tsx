import React, { useState } from 'react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface InputChatProps {
    currentMessage: string;
    onChange: (e: string[]) => void;
}

const InputChat = ({ currentMessage, onChange }: InputChatProps) => {
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
                onChange([...currentMessage, value]);
                setValue('');
            }}>
                Send
            </Button>
        </section>
    );
};

export default InputChat;