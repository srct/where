import { PointOfInterest } from '../models/point_of_interest.model';
import { PoiAction, PoiActionTypes } from './poi.actions';

export interface PoiState {
    pointsOfInterest: PointOfInterest[];
}

const initialState: PoiState = {
    pointsOfInterest: []
};

export function PoiReducer(state = initialState, action: PoiAction) {
    switch (action.type) {
        case PoiActionTypes.ADD_POI:
            return {
                ...state,
                pointsOfInterest: [...state.pointsOfInterest, action.payload]
            };
        default:
            return state;
    }
}
