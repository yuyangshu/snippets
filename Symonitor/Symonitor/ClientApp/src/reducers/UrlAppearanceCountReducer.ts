import { Action, Reducer } from 'redux';
import { KnownAction } from '../actions/UrlAppearanceCountActions'
import { UrlAppearanceCountState } from '../store/UrlAppearanceCountState'

// ----------------
// REDUCER - For a given state and action, returns the new state. To support time travel, this must not mutate the old state.

const unloadedState: UrlAppearanceCountState = { urlAppearanceCounts: [], isLoading: false };

export const reducer: Reducer<UrlAppearanceCountState> = (state: UrlAppearanceCountState | undefined, incomingAction: Action): UrlAppearanceCountState => {
    if (state === undefined) {
        return unloadedState;
    }

    const action = incomingAction as KnownAction;
    switch (action.type) {
        case 'REQUEST_URL_APPEARANCE_COUNTS':
            return {
                urlAppearanceCounts: state.urlAppearanceCounts,
                isLoading: true
            };
        case 'RECEIVE_URL_APPEARANCE_COUNTS':
            let index = state.urlAppearanceCounts.findIndex(
                x => x.keywords === action.appearanceCount.keywords && x.url === action.appearanceCount.url
            );

            if (~index) {
                state.urlAppearanceCounts[index] = action.appearanceCount;
                return {
                    urlAppearanceCounts: state.urlAppearanceCounts,
                    isLoading: false
                };
            }

            return {
                urlAppearanceCounts: [
                    ...state.urlAppearanceCounts,
                    action.appearanceCount
                ],
                isLoading: false
            };
        default:
            return state;
    }
};
