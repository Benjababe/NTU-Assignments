import React, { useRef } from "react";
import { EtcObject, createObject } from "../services/objects";
import classes from "../assets/styles/addwindow.module.css";
import { User } from "../services/user";

interface AddWindowProps {
    user: User
    selfMarker: EtcObject;
    setSelfMarker: React.Dispatch<React.SetStateAction<EtcObject>>;
    markers: EtcObject[];
    setMarkers: React.Dispatch<React.SetStateAction<EtcObject[]>>
    mapType: string;
    setEnableAddWindow: React.Dispatch<React.SetStateAction<boolean>>;
}

export const AddWindow = ({ user, selfMarker, setSelfMarker, markers, setMarkers, mapType, setEnableAddWindow }: AddWindowProps) => {
    const txtLevelRef = useRef<HTMLInputElement>(null);
    const txtCommentsRef = useRef<HTMLTextAreaElement>(null);
    const imgUploadRef = useRef<HTMLInputElement>(null);

    const addObject = async () => {
        const etcObject: EtcObject = {
            user_id: user.userId,
            type: mapType,
            lat: selfMarker.lat,
            lng: selfMarker.lng,
            level: txtLevelRef.current.value.trim(),
            comments: txtCommentsRef.current.value.trim(),
            images: imgUploadRef.current.files,
        };

        const res = await createObject(user, etcObject);
        if (res.success) {
            if (res.approved) {
                etcObject.id = res.etcObjectId;
                setMarkers(markers.concat(etcObject));
            } else {
                alert("Newly added object requires to be vetted before it's shown on the map");
            }
            setSelfMarker(null);
        } else {
            alert(res.error);
        }
    };

    return (
        <div className={classes.AddWindowContainer}>
            <div
                className={classes.AddWindowModal}
                onClick={() => setEnableAddWindow(false)} />
            <div className={classes.AddWindow}>
                <h2 className={classes.AddWindowHeader}>Add Etc Object</h2>

                <label>Type:</label>
                <input type="text" value={mapType} disabled />

                <label>Lat: </label>
                <input type="text" value={selfMarker.lat} disabled />

                <label>Lng: </label>
                <input type="text" value={selfMarker.lng} disabled />

                <label>Level: </label>
                <input ref={txtLevelRef} type="text" placeholder="B1" />

                <label>Comments: </label>
                <textarea ref={txtCommentsRef} placeholder="Describe the location" />

                <label>Images: </label>
                <input ref={imgUploadRef} type="file" multiple />

                <button
                    onClick={() => addObject()}>
                    Submit
                </button>
            </div>
        </div>
    );
};