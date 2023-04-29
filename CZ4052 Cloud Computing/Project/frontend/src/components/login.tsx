import React, { useRef, useCallback } from "react";
import userService, { User } from "../services/user";
import classes from "../assets/styles/login.module.css";
import bClasses from "../assets/styles/button.module.css";

interface LoginProps {
    user: User;
    setUser: React.Dispatch<React.SetStateAction<User>>;
}

export const Login = ({ user, setUser }: LoginProps) => {
    const usernameRef = useRef<HTMLInputElement>();
    const passwordRef = useRef<HTMLInputElement>();
    const statusRef = useRef<HTMLDivElement>();

    const showSuccess = (msg: string, timeMs: number) => {
        statusRef.current.className = classes.Success;
        statusRef.current.textContent = msg;
        setTimeout(() => {
            statusRef.current.textContent = "";
        }, timeMs);
    };

    const showError = (msg: string, timeMs: number) => {
        statusRef.current.className = classes.Error;
        statusRef.current.textContent = msg;
        setTimeout(() => {
            statusRef.current.textContent = "";
        }, timeMs);
    };

    const register = useCallback(async () => {
        const username = usernameRef.current.value.trim();
        const password = passwordRef.current.value.trim();

        if (username.length == 0 && password.length == 0)
            return;

        const res = await userService.register(username, password);

        if (res.success)
            showSuccess("Registration Successful", 3000);
        else
            showError(res.error, 3000);
    }, [usernameRef, passwordRef]);

    const login = useCallback(async () => {
        const username = usernameRef.current.value.trim();
        const password = passwordRef.current.value.trim();

        if (username.length == 0 && password.length == 0)
            return;

        const res = await userService.login(username, password);

        if (res.success) {
            showSuccess(`Logged in as ${res.user.username}`, 3000);
            setUser(res.user);
            localStorage.setItem("user", JSON.stringify(res.user));
        } else {
            showError(res.error, 3000);
        }
    }, [usernameRef, passwordRef]);

    const logout = () => {
        setUser(null);
        localStorage.removeItem("user");
    };

    const checkReputation = async () => {
        const res = await userService.checkReputation(user.userId);
        if (res.success)
            alert(`Your reputation score is ${res.reputationScore.toFixed(2)}`);
        else
            showError(res.error, 3000);
    };

    return (
        <div className={classes.LoginContainer}>
            <div ref={statusRef}></div>
            {
                (user) ?
                    <div className={classes.LoggedIn}>
                        You are logged in as {user.username}
                        <button
                            className={`${classes.LogoutBtn} ${bClasses.ResponsiveButton}`}
                            onClick={logout}>
                            Logout
                        </button>
                        <button
                            className={`${classes.RepBtn} ${bClasses.ResponsiveButton}`}
                            onClick={checkReputation}>
                            Check Reputation
                        </button>
                    </div>
                    :
                    <div className={classes.LoginField}>
                        <label>Username:</label>
                        <input ref={usernameRef} type="text" />

                        <label>Password:</label>
                        <input ref={passwordRef} type="password" />
                        <div className={classes.LoginSubmit}>
                            <button
                                className={`${classes.LoginSubmitBtn} ${bClasses.ResponsiveButton}`}
                                onClick={register}>
                                Register
                            </button>
                            <button
                                className={`${classes.LoginSubmitBtn} ${bClasses.ResponsiveButton}`}
                                onClick={login}>
                                Login
                            </button>
                        </div>
                    </div>
            }
        </div>
    );
};