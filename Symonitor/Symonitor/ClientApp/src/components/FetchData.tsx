import * as React from 'react';
import { connect } from 'react-redux';
import { UrlAppearanceForm } from './UrlApperanceForm';
import { ApplicationState } from '../store';
import { UrlAppearanceCount } from '../models/UrlAppearanceCountsModels';
import { UrlAppearanceCountState } from '../store/UrlAppearanceCountState';
import * as UrlAppearanceCountActions from '../actions/UrlAppearanceCountActions';

// At runtime, Redux will merge together...
type UrlAppearanceCountProps =
UrlAppearanceCountState // ... state we've requested from the Redux store
    & typeof UrlAppearanceCountActions.actionCreators // ... plus action creators we've requested


class FetchData extends React.PureComponent<UrlAppearanceCountProps> {
    public render() {
        return (
            <React.Fragment>
                <h1 id="tabelLabel">Symonitor</h1>
                <br></br>
                <p> This page displays the number of appearances of a URL in the first 100 results on Google, given a set of keywords. </p>
                {this.renderUrlAppearanceCountsTable()}
                <br></br>
                <UrlAppearanceForm requestUrlAppearanceCounts={this.props.requestUrlAppearanceCounts} />
            </React.Fragment>
        );
    }

    private renderUrlAppearanceCountsTable() {
        if (this.props.isLoading) {
            return (
                <span>Loading...</span>
            );
        }

        return (
            <table className='table table-striped' aria-labelledby="tabelLabel">
                <thead>
                    <tr>
                        <th>Keywords</th>
                        <th>Url</th>
                        <th>Count</th>
                    </tr>
                </thead>
                <tbody>
                    {this.props.urlAppearanceCounts.map((count: UrlAppearanceCount) =>
                        <tr key={count.url}>
                            <td>{count.keywords}</td>
                            <td>{count.url}</td>
                            <td>{count.count}</td>
                        </tr>
                    )}
                </tbody>
            </table>
        );
    }
}

export default connect(
    (state: ApplicationState) => state.urlAppearanceCounts, // Selects which state properties are merged into the component's props
    UrlAppearanceCountActions.actionCreators // Selects which action creators are merged into the component's props
)(FetchData as any);
