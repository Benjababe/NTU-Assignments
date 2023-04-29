import React, { useState, useEffect, useCallback } from "react";
import { GoogleMap, LoadScript, Marker, MarkerF, MarkerClustererF } from "@react-google-maps/api";
import { AddButton } from "./addetcbutton";
import { AddWindow } from "./addwindow";
import { SideBar } from "./sidebar";
import { User } from "../services/user";
import { EtcObject, getEtcObjects } from "../services/objects";

import waterFountainIcon from "../assets/images/icons/water-fountain.svg";
import vendingMachineIcon from "../assets/images/icons/vending-machine.svg";
import publicShowerIcon from "../assets/images/icons/public-shower.svg";
import classes from "../assets/styles/etcmap.module.css";
import { VoteWindow } from "./votewindow";
import { CurrentLocation, CurrentLocationMarker } from "./currentlocationmarker";
import { CurrentLocationButton } from "./currentlocationbutton";

const MAPS_API_KEY = process.env.REACT_APP_MAPS_API_KEY;
const MAP_STYLE_ID = process.env.REACT_APP_MAPS_STYLE_ID;

interface MapIcons {
    [key: string]: string;
}

const ICONS: MapIcons = {
    "Water Fountain": waterFountainIcon,
    "Vending Machine (Food)": vendingMachineIcon,
    "Vending Machine (Drinks)": vendingMachineIcon,
    "Public Shower": publicShowerIcon,
};

const MAP_OPTIONS: google.maps.MapOptions = {
    clickableIcons: false,
    disableDefaultUI: true,
    disableDoubleClickZoom: true,
    mapId: MAP_STYLE_ID,
    streetViewControl: true,
    zoom: 17,
    zoomControl: true,
};


const EtcMap = () => {
    const [map, setMap] = useState<google.maps.Map>(null);
    const [mapType, setMapType] = useState<string>("Vending Machine (Drinks)");
    const [selfMarker, setSelfMarker] = useState<EtcObject>(null);
    const [activeEtcObject, setActiveEtcObject] = useState<EtcObject>(null);
    const [etcObjects, setEtcObjects] = useState<EtcObject[]>([]);
    const [currentLocation, setCurrentLocation] = useState<CurrentLocation>({ lat: 1.346165, lng: 103.682020, accuracy: 0 });
    const [enableAddWindow, setEnableAddWindow] = useState(false);
    const [user, setUser] = useState<User>(null);

    const getCurrentPosition = () => {
        console.log("Getting current pos...");
        navigator?.geolocation.getCurrentPosition(
            ({ coords }) => {
                const { latitude, longitude, accuracy } = coords;
                setCurrentLocation({ lat: latitude, lng: longitude, accuracy: accuracy });
            },
            (error) => console.error(error)
        );
    };

    // tries to set map location to current GPS location
    useEffect(() => {
        getCurrentPosition();
    }, [map]);

    // retrieves stored logged in user info
    useEffect(() => {
        const user = localStorage.getItem("user");
        if (user !== null)
            setUser(JSON.parse(user));
    }, []);

    // when map type is changed, retrieve the markers for the new type
    // run for user change as well to retrieve votes
    useEffect(() => {
        if (map !== null) {
            getEtcObjects(mapType).then((etcObjects) => {
                setEtcObjects(etcObjects);
            });
        }
    }, [mapType, user]);

    // on map load, retrieve the markers for the initial type
    const onLoad = useCallback((map: google.maps.Map) => {
        setMap(map);
        getEtcObjects(mapType).then((etcObjects) => {
            setEtcObjects(etcObjects);
        });
    }, []);

    const onUnmount = useCallback(() => {
        setMap(null);
    }, []);

    // when map is clicked, add/remove the self marker and hide the voting window
    const onMapClick = useCallback((e: google.maps.MapMouseEvent) => {
        if (user !== null && selfMarker === null)
            setSelfMarker(e.latLng.toJSON());
        else
            setSelfMarker(null);

        setActiveEtcObject(null);
    }, [user, selfMarker]);

    const showAddWindow = () => {
        setEnableAddWindow(true);
    };

    // when an existing marker is clicked, show the voting window
    const onMarkerClick = useCallback((etcObject: EtcObject) => {
        if (activeEtcObject !== null)
            setActiveEtcObject(null);
        else
            setActiveEtcObject(etcObject);
    }, [activeEtcObject]);

    const clustererOptions = {
        gridSize: 30
    };

    return (
        <div>
            <LoadScript
                googleMapsApiKey={MAPS_API_KEY}
                mapIds={[MAP_STYLE_ID]}>
                <GoogleMap
                    mapContainerClassName={classes.MapContainer}
                    center={currentLocation}
                    options={MAP_OPTIONS}
                    onLoad={onLoad}
                    onUnmount={onUnmount}
                    onClick={onMapClick}>
                    {(selfMarker !== null) ?
                        <MarkerF
                            key="self-marker"
                            position={selfMarker}
                            onDragEnd={(e) => { setSelfMarker(e.latLng.toJSON()); }}
                            draggable={true} /> : ""}
                    {(etcObjects.length > 0) ?
                        <MarkerClustererF options={clustererOptions}>
                            {(clusterer) => (
                                <>
                                    {etcObjects.map((etcObject, i) => {
                                        return <Marker
                                            key={i}
                                            position={{ lat: etcObject.lat, lng: etcObject.lng }}
                                            visible={true}
                                            icon={ICONS[mapType]}
                                            onClick={() => onMarkerClick(etcObject)}
                                            clusterer={clusterer} />;
                                    })}
                                </>
                            )}
                        </MarkerClustererF> : ""
                    }
                    <CurrentLocationMarker location={currentLocation} />
                    <AddButton
                        showBtn={(selfMarker !== null)}
                        showAddWindow={showAddWindow} />
                    <CurrentLocationButton
                        map={map}
                        getCurrentLocation={getCurrentPosition} />
                </GoogleMap>
                {
                    (enableAddWindow && selfMarker) ?
                        <AddWindow
                            user={user}
                            selfMarker={selfMarker}
                            setSelfMarker={setSelfMarker}
                            markers={etcObjects}
                            setMarkers={setEtcObjects}
                            mapType={mapType}
                            setEnableAddWindow={setEnableAddWindow} /> : ""
                }
                <VoteWindow
                    user={user}
                    etcObject={activeEtcObject}
                    etcObjects={etcObjects}
                    setEtcObject={setActiveEtcObject}
                    setEtcObjects={setEtcObjects} />
            </LoadScript>
            <SideBar
                user={user}
                setUser={setUser}
                setMapType={setMapType} />
        </div>
    );
};

export default EtcMap;