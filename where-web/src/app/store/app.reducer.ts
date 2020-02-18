import { ActionReducerMap } from '@ngrx/store';
import { PoiState, PoiReducer } from './poi.reducer';

export interface AppState {
    poi: PoiState;
}

export const reducers: ActionReducerMap<AppState, any> = {
    poi: PoiReducer
};
