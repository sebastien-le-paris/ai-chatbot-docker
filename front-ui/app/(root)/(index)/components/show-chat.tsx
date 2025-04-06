import React, { ReactNode } from 'react';

import { ScrollArea } from '@/components/ui/scroll-area';

interface ShowChatProps {
    children: ReactNode; // children is a prop that can be used to render the component
}

const ShowChat = ({ children }: ShowChatProps) => {
    return (
        <div>
            <ScrollArea className="h-[70vh] container mx-auto rounded-lg bg-cyan-50 border-2 border-foreground">
                {children}
            </ScrollArea>
        </div>
    );
};

export default ShowChat;