export const baseUrl = (!process.env.NODE_ENV || process.env.NODE_ENV === "development")
    ? "http://localhost:3001"
    : "";

