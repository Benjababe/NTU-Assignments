import React from "react";
import { CircleF, MarkerF } from "@react-google-maps/api";
import colours from "../assets/design/colours";

interface CurrentLocationMarkerProps {
    location: CurrentLocation;
}

export interface CurrentLocation {
    lat: number;
    lng: number;
    accuracy: number;
}

export const CurrentLocationMarker = ({ location }: CurrentLocationMarkerProps) => {
    const blueDot = {
        fillColor: colours["google-blue 100"],
        fillOpacity: 1,
        path: google.maps.SymbolPath.CIRCLE,
        scale: 8,
        strokeColor: colours["white 100"],
        strokeWeight: 2,
    };

    const radiusCircle = {
        center: location,
        fillColor: colours["google-blue-dark 100"],
        fillOpacity: 0.4,
        radius: location.accuracy,
        strokeColor: colours["google-blue-light 100"],
        strokeOpacity: 0.4,
        strokeWeight: 1,
        zIndex: 1,
    };

    return (
        <>
            <MarkerF
                icon={blueDot}
                position={location} />
            <CircleF
                options={radiusCircle} />
        </>
    );
};