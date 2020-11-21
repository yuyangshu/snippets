import { AppThunkAction } from './AppThunkAction';
import { UrlAppearanceCount, UrlAppearanceQuery } from '../models/UrlAppearanceCountsModels'

interface RequestUrlAppearanceCountsAction {
    type: 'REQUEST_URL_APPEARANCE_COUNTS';
}

interface ReceiveUrlAppearanceCountsAction {
    type: 'RECEIVE_URL_APPEARANCE_COUNTS';
    appearanceCount: UrlAppearanceCount;
}

// Declare a 'discriminated union' type. This guarantees that all references to 'type' properties contain one of the
// declared type strings (and not any other arbitrary string).
export type KnownAction = RequestUrlAppearanceCountsAction | ReceiveUrlAppearanceCountsAction;

// ----------------
// ACTION CREATORS - These are functions exposed to UI components that will trigger a state transition.
// They don't directly mutate state, but they can have external side-effects (such as loading data).

export const actionCreators = {
    requestUrlAppearanceCounts: (query: UrlAppearanceQuery): AppThunkAction<KnownAction> => (dispatch) => {
        fetch(
            `UrlAppearance/CountAppearances`,
            {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    Keywords: query.keywords,
                    Url: query.url
                })
            }
        )
        .then(response => response.json() as Promise<UrlAppearanceCount>)
        .then(data => {
            dispatch({ type: 'RECEIVE_URL_APPEARANCE_COUNTS', appearanceCount: data });
        });

        dispatch({ type: 'REQUEST_URL_APPEARANCE_COUNTS' });
    }
};
