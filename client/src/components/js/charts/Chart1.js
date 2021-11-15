import React, { Component } from "react";
import Chart from "react-google-charts";
// import logo from "img.JPG"

class Chart1 extends Component {
    
    constructor(props) {
        super();
        
        this.state = {
            error: null,
            isLoaded: false,
            chartData: [],
            sentimentData: [],
            full_data: [],
        };
    }
    getChartData = () => {
        fetch("http://127.0.0.1:5000/mostmentioned/10")
            .then((response) => response.json())
            .then(
                (result) => {
                    const json = result;
                    const rateCurrencyNames = Object.keys(json.result)
                    const rateCurrencyValues = Object.values(json.result)
                    const chartData = [['Company', 'Frequency']]
                    for (let i = 0; i < rateCurrencyNames.length; i += 1) {
                        chartData.push([rateCurrencyValues[i].Company_Name, parseInt(rateCurrencyValues[i].Frequency)]);
                    }
                    this.setState({
                        isLoaded: true,
                        chartData: chartData,
                        sentimentData: result.result,
                    });
                    console.log(chartData);
                    console.log(result);
                    
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error,
                    });
                }
            );
            
    };
    getSentimentData = () => {
        fetch("http://127.0.0.1:5000/mostsentimental/10")
            .then((response) => response.json())
            .then(
                (result) => {
                    const json = result;
                    const rateCurrencyNames = Object.keys(json.result)
                    const rateCurrencyValues = Object.values(json.result)
                    const sentimentData = [['Company', 'Sentiment', 'Frequency']]
                    for (let i = 0; i < rateCurrencyNames.length; i += 1) {
                        sentimentData.push([rateCurrencyValues[i].Company_Name, parseFloat(rateCurrencyValues[i].Sentiment), parseInt(rateCurrencyValues[i].Frequency)]);
                    }
                    this.setState({
                        isLoaded: true,
                        sentimentData: sentimentData,
                    });
                    console.log(sentimentData);
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error,
                    });
                }
            );
            
    };

    componentDidMount() {
        this.getChartData();
        this.getSentimentData();
    }
    render() {
        if (this.state.error) {
            return <div>Error: {this.state.error.message}</div>;
        } else if (!this.state.isLoaded) {
            return (
                <div className="spinner-border" role="status">
                    <span className="sr-only">Loading...</span>
                </div>
            );
        } else {
            return (
                <React.Fragment>
                    <div style={{ display: 'flex', alignItems: "center"}}>
                    <Chart
                        width={'700px'}
                        height={'400px'}
                        chartType="PieChart"
                        loader={<div>Loading Chart</div>}
                        data={this.state.chartData}
                        options={{
                            title: 'Top 10 Stocks discussed on Social Media',
                            // Just add this option
                            is3D: true,
                        }}
                        rootProps={{ 'data-testid': '3' }}
                    />
                    <Chart
                        width={'500px'}
                        height={'400px'}
                        chartType="ColumnChart"
                        loader={<div>Loading Chart</div>}
                        data={this.state.sentimentData}
                        options={{
                        title: 'Top 10 Sentimental stocks with their frequency',
                        
                        hAxis: {
                            title: 'Sentimental Analysis',
                            minValue: 0,
                        },
                        vAxis: {
                            title: 'Frequency/Sentiment Value',
                        },
                        }}
                        legendToggle
                    />
                    
                    </div>
                    {/* <div>
                        <img src={process.env.PUBLIC_URL +'/components/js/charts/img.JPG'} height='400px' width='400px'></img>
                    </div> */}
                </React.Fragment>
            );
        }
    }
}

export default Chart1;