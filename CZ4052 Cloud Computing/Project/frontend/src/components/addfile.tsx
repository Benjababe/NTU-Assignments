import React, { useState } from "react";
import classes from "../assets/styles/addfile.module.css";
import bClasses from "../assets/styles/button.module.css";
import { EtcObject, createObjectBulk } from "../services/objects";
import { User } from "../services/user";

interface AddFileProps {
    user: User;
    mapType: string;
}

export const AddFile = ({ user, mapType }: AddFileProps) => {
    const [toAdd, setToAdd] = useState<EtcObject[]>([]);

    const readFileContent = (e: ProgressEvent<FileReader>) => {
        const content = e.target.result.toString().split("\n");
        const contentJson = content.map((obj) => JSON.parse(obj));
        setToAdd(contentJson);
    };

    const onFileChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
        const filePicker = e.target;
        const file = filePicker.files[0];

        const reader = new FileReader();
        reader.onload = readFileContent;
        reader.readAsText(file);
    };

    const uploadFile: React.MouseEventHandler<HTMLButtonElement> = () => {
        createObjectBulk(user, mapType, toAdd);
    };

    // temporarily removing it
    return <></>;

    return (
        <div className={classes.AddFileContainer}>
            <input
                className={classes.AddFileSelector}
                onChange={onFileChange}
                type="file"
                accept=".txt, application/json" />
            {
                (toAdd.length > 0)
                    ?
                    <>
                        <select
                            className={classes.AddFileList}
                            size={Math.min(toAdd.length, 15)}>
                            {
                                toAdd.map((el, i) => {
                                    return (<option key={i}>{JSON.stringify(el)}</option>);
                                })
                            }
                        </select>
                        <button
                            className={`${classes.UploadBtn} ${bClasses.ResponsiveButton}`}
                            onClick={uploadFile}>
                            Upload
                        </button>
                    </>
                    : ""
            }
        </div>
    );
};