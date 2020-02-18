import { Action } from '@ngrx/store';
import { PointOfInterest } from '../models/point_of_interest.model';

export enum PoiActionTypes {
    ADD_POI = '[POI] Add poi'
}

export class AddPoi implements Action {
    readonly type = PoiActionTypes.ADD_POI;

    constructor(public payload: PointOfInterest) {}
}

export type PoiAction = AddPoi;
