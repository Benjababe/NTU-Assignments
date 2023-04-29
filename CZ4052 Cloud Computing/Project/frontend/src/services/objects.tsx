import { baseUrl } from "./constants";
import { User } from "./user";

const objectUrl = `${baseUrl}/api/objects`;
const objectBulkUrl = `${baseUrl}/api/objects/bulk`;
const voteUrl = `${baseUrl}/api/objectVote`;

interface VoteResponse {
    success: boolean;
    voteVal?: number;
}

interface DeleteResponse {
    success: boolean;
    etcObjectId?: number;
    error?: string;
}

interface CreateEtcObjectResponse {
    success: boolean;
    etcObjectId?: number;
    approved?: boolean;
    error?: string;
}

interface CreateEtcObjectBulkResponse {
    success: boolean;
    etcObjects?: EtcObject[];
    approved?: boolean;
    error?: string;
}

export interface EtcObject {
    id?: number;
    user_id?: number;
    user?: string;
    type?: string;
    name?: string;
    lat: number;
    lng: number;
    level?: string;
    comments?: string;
    voted?: number;
    images?: FileList;
    paths?: string[];
}

export const getEtcObjects = async (mapType: string): Promise<EtcObject[]> => {
    const url = `${objectUrl}?map_type=${mapType}`;
    const res = await fetch(url);
    const data: EtcObject[] = await res.json();

    return data;
};

export const createObject = async (user: User, etcObject: EtcObject): Promise<CreateEtcObjectResponse> => {
    const formData = new FormData();
    formData.append("type", etcObject.type);
    formData.append("lat", etcObject.lat.toString());
    formData.append("lng", etcObject.lng.toString());
    formData.append("level", etcObject.level);
    formData.append("comments", etcObject.comments);

    for (const image of etcObject.images) {
        formData.append("images", image);
    }

    const options = {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${user.authToken}`,
        },
        body: formData,
    };

    const res = await fetch(objectUrl, options);
    const data = await res.json();

    return data;
};

export const createObjectBulk = async (user: User, mapType: string, etcObjects: EtcObject[]): Promise<CreateEtcObjectBulkResponse> => {
    const options = {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${user.authToken}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ mapType: mapType, etcObjects: etcObjects }),
    };

    const res = await fetch(objectBulkUrl, options);
    const data = await res.json();

    return data;
};

export const voteObject = async (user: User, etcObjectId: number, voteVal: number): Promise<VoteResponse> => {
    const options = {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${user.authToken}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ etcObjectId: etcObjectId, voteVal: voteVal }),
    };

    const res = await fetch(voteUrl, options);
    const data = await res.json();

    return data;
};

export const deleteObject = async (user: User, etcObjectId: number): Promise<DeleteResponse> => {
    const options = {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${user.authToken}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ etcObjectId: etcObjectId }),
    };

    const res = await fetch(objectUrl, options);
    const data = await res.json();

    return data;
};