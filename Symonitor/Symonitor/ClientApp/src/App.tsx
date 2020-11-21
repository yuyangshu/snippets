import * as React from 'react';
import { Route } from 'react-router';
import Layout from './components/Layout';
import FetchData from './components/FetchData';

export default () => (
    <Layout>
        <Route exact path='/' component={FetchData} />
    </Layout>
);
