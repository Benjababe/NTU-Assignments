import React, { useRef, useEffect } from "react";
import classes from "../assets/styles/currentlocationbutton.module.css";
import locationIcon from "../assets/images/icons/location.svg";

interface CurrentLocationButtonProps {
    map: google.maps.Map,
    getCurrentLocation: () => void,
}

export const CurrentLocationButton = ({ map, getCurrentLocation }: CurrentLocationButtonProps) => {
    const ref = useRef();

    useEffect(() => {
        if (map && ref) {
            const position = window.google.maps.ControlPosition.RIGHT_BOTTOM;
            map.controls[position].push(
                ref.current
            );
        }
    }, [map, ref]);

    return (
        <button
            ref={ref}
            onClick={() => getCurrentLocation()}
            className={classes.CurrentLocationButton}>
            <img
                src={locationIcon}
                className={classes.CurrentLocationImage} />
        </button>
    );
};