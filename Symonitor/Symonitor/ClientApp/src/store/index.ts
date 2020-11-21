import { UrlAppearanceCountState } from './UrlAppearanceCountState';
import * as UrlAppearanceCountReducer from '../reducers/UrlAppearanceCountReducer';

// The top-level state object
export interface ApplicationState {
    urlAppearanceCounts: UrlAppearanceCountState | undefined;
}

// Whenever an action is dispatched, Redux will update each top-level application state property using
// the reducer with the matching name. It's important that the names match exactly, and that the reducer
// acts on the corresponding ApplicationState property type.
export const reducers = {
    urlAppearanceCounts: UrlAppearanceCountReducer.reducer
};
