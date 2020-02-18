export interface PointOfInterest {
    id: number;
    name: string;
    floor: number | null;
    category: string;
    parent: number;
    lat: number;
    lon: number;
};
