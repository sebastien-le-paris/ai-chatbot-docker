import { Card, CardContent } from '@/components/ui/card';

import React from 'react';

interface MessageChatProps {
    result: string; // result is the message from the AI
    user: string; // user is the message from the user
}   

const MessageChat = ({ result, user }: MessageChatProps) => {
    return (
        <Card>
            <CardContent>
                {result}
            </CardContent>
        </Card>
    );
};

export default MessageChat;