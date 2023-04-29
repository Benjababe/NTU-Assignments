import React, { SyntheticEvent } from "react";
import { EtcObject, deleteObject, voteObject } from "../services/objects";
import classes from "../assets/styles/votewindow.module.css";
import { User } from "../services/user";
import { baseUrl } from "../services/constants";

import voteUpIcon from "../assets/images/icons/vote-up.svg";
import voteDownIcon from "../assets/images/icons/vote-down.svg";
import ImageGallery, { ReactImageGalleryItem } from "react-image-gallery";
import "react-image-gallery/styles/css/image-gallery.css";

interface VoteWindowProps {
    user: User,
    etcObject: EtcObject,
    etcObjects: EtcObject[],
    setEtcObject: React.Dispatch<React.SetStateAction<EtcObject>>,
    setEtcObjects: React.Dispatch<React.SetStateAction<EtcObject[]>>,
}

export const VoteWindow = ({ user, etcObject, etcObjects, setEtcObject, setEtcObjects }: VoteWindowProps) => {
    const voteEtcObject = async (voteVal: number) => {
        const res = await voteObject(user, etcObject.id, voteVal);
        if (res.success) {
            const updatedEtcObjects = etcObjects.map((eo) => {
                if (eo.id == etcObject.id)
                    eo.voted = res.voteVal;
                return eo;
            });
            setEtcObjects(updatedEtcObjects);
        }
    };

    const images: ReactImageGalleryItem[] = (etcObject && etcObject.paths) ?
        etcObject.paths.map((path) => {
            return {
                original: `${baseUrl}${path}`,
                originalWidth: 100,
                originalHeight: 100
            };
        })
        : [];

    const onImageClick = (e: SyntheticEvent) => {
        const img = e.target as HTMLImageElement;
        window.open(img.currentSrc, "_blank");
    };

    const onDeleteButtonClicked = async () => {
        const res = await deleteObject(user, etcObject.id);
        if (res.success) {
            console.log(etcObjects);
            setEtcObjects(etcObjects.filter(obj => obj.id !== etcObject.id));
            setEtcObject(null);
        } else {
            alert(res.error);
        }
    };

    return (
        <div className={`${classes.VoteWindow} ${(images.length > 0) ? classes.VoteWindowImages : ""} ${(etcObject !== null) ? classes.VoteWindowShow : ""}`}>
            {(etcObject === null) ? "" :
                <>
                    <h2>{etcObject.type}</h2>
                    <h3>{etcObject.name}</h3>
                    <div>
                        <div className={classes.DetailRow}>
                            <span>Level:</span>
                            <span>{etcObject.level}</span>
                        </div>
                        <div className={classes.DetailRow}>
                            <span>Comments:</span>
                            <span>{etcObject.comments}</span>
                        </div>
                        {
                            (images.length > 0) ?
                                <div className={classes.ImageRow}>
                                    <ImageGallery
                                        items={images}
                                        infinite={true}
                                        showThumbnails={false}
                                        showBullets={true}
                                        showPlayButton={false}
                                        showFullscreenButton={false}
                                        onClick={onImageClick} />
                                </div>
                                : ""
                        }
                    </div>
                    {
                        (user !== null && user.userId !== etcObject.user_id)
                            ?
                            <div className={classes.VoteContainer}>
                                <div>Submitted by: {etcObject.user}</div>
                                <div className={classes.VoteBox}>
                                    <img
                                        className={`${classes.VoteIcon} ${(etcObject.voted == 1) ? classes.VoteUp : ""}`}
                                        src={voteUpIcon}
                                        onClick={() => voteEtcObject(1)} />
                                    <img
                                        className={`${classes.VoteIcon} ${(etcObject.voted == -1) ? classes.VoteDown : ""}`}
                                        src={voteDownIcon}
                                        onClick={() => voteEtcObject(-1)} />
                                </div>
                            </div>
                            :
                            <div className={classes.DeleteContainer}>
                                <button
                                    onClick={onDeleteButtonClicked}
                                    className={classes.DeleteButton}>
                                    Delete Object
                                </button>
                            </div>
                    }
                </>
            }
        </div>
    );
};