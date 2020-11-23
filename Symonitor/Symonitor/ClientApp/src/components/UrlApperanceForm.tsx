import * as React from 'react';
import * as UrlAppearanceCountActions from '../actions/UrlAppearanceCountActions';

type UrlAppearanceFormProps = typeof UrlAppearanceCountActions.actionCreators

interface UrlAppearanceFormState {
    keywords: string,
    url: string
}



export class UrlAppearanceForm extends React.PureComponent<UrlAppearanceFormProps, UrlAppearanceFormState> {
    constructor(props: UrlAppearanceFormProps) {
        super(props);
        this.state = { keywords: '', url: '' };

        this.handleKeywordsChange = this.handleKeywordsChange.bind(this);
        this.handleUrlChange = this.handleUrlChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    private handleKeywordsChange = (event: React.FormEvent<HTMLInputElement>): void => {
        this.setState({
            ...this.state,
            keywords: event.currentTarget.value
        });
    };

    private handleUrlChange = (event: React.FormEvent<HTMLInputElement>): void => {
        this.setState({
            ...this.state,
            url: event.currentTarget.value
        });
    };

    private handleSubmit(event: React.SyntheticEvent) {
        event.preventDefault();
        this.props.requestUrlAppearanceCounts(this.state);
    }

    

    public render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <h2> Add Url Appearance Count Entry </h2>
                <br></br>
                <p> Add a pair of (keywords, url) to count. </p>
                <label>
                    Keywords:
                    <input type="text" value={this.state.keywords} onChange={this.handleKeywordsChange} />
                </label> <br/>
                <label>
                    Url:
                    <input type="text" value={this.state.url} onChange={this.handleUrlChange} />
                </label> <br/>
                <input className="btn btn-primary" type="submit" value="Submit" />
            </form>
        );
    }
}