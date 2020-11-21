import { UrlAppearanceCount } from '../models/UrlAppearanceCountsModels';

// -----------------
// STATE - This defines the type of data maintained in the Redux store.

export interface UrlAppearanceCountState {
    isLoading: boolean;
    urlAppearanceCounts: UrlAppearanceCount[];
}
