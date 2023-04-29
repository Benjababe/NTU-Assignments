import { baseUrl } from "./constants";

const registerUrl = `${baseUrl}/api/register`;
const loginUrl = `${baseUrl}/api/login`;
const reputationUrl = `${baseUrl}/api/reputation`;

export interface User {
    username: string;
    authToken: string;
    userId: number;
}

interface RegisterResponse {
    success: boolean;
    error?: string;
}

interface LoginResponse {
    success: boolean;
    error?: string;
    user?: User;
}

interface ReputationResponse {
    success: boolean;
    error?: string;
    reputationScore: number;
}

const register = async (username: string, password: string): Promise<RegisterResponse> => {
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password }),
    };

    const res = await fetch(registerUrl, options);
    const data = await res.json();

    return data;
};

const login = async (username: string, password: string): Promise<LoginResponse> => {
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password }),
    };

    const res = await fetch(loginUrl, options);
    const data = await res.json();

    return data;
};

const checkReputation = async (userId: number): Promise<ReputationResponse> => {
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId: userId }),
    };

    const res = await fetch(reputationUrl, options);
    const data = await res.json();

    return data;
};

export default {
    register,
    login,
    checkReputation,
};