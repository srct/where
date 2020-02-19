import { createFeatureSelector } from '@ngrx/store';
import { PoiState } from './poi.reducer';

const getPoiState = createFeatureSelector<PoiState>('poi');