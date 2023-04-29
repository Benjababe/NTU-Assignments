import React from "react";
import classes from "../assets/styles/addetcbutton.module.css";

interface AddButtonProps {
    showBtn: boolean;
    showAddWindow: (e: React.MouseEvent) => void;
}

export const AddButton = ({ showBtn, showAddWindow }: AddButtonProps) => {
    return (
        <>
            <button
                className={`${classes.AddBtn} ${(!showBtn) ? classes.BtnHide : ""}`}
                onClick={(e) => showAddWindow(e)}>
                Add Object Here
            </button>
        </>
    );
};