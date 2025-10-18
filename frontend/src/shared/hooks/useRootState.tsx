import { useState } from "react";

export const useRootState = () => {
    const [name, setName] = useState('');

    return {
        name,
        setName
    };
};
