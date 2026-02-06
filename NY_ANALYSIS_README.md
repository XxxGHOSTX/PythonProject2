# NY Data Deep Analysis Module

## Overview

The `ny_analysis.py` module provides comprehensive data analysis capabilities for datasets, with a focus on New York (NY) data analysis. It includes statistical analysis, outlier detection, correlation analysis, trend detection, and automated insight generation.

## Features

### 1. Basic Statistical Analysis
- Calculate mean, median, standard deviation
- Min/max values and quartiles
- Automatic detection of numeric vs categorical fields
- Frequency analysis for categorical data

### 2. Outlier Detection
- **IQR Method**: Interquartile Range-based detection
- **Z-Score Method**: Standard deviation-based detection
- Identifies data points that deviate significantly from the norm

### 3. Correlation Analysis
- Pearson correlation coefficient calculation
- Automatic strength classification (strong/moderate/weak)
- Direction detection (positive/negative)

### 4. Trend Analysis
- Time-series trend detection
- Linear regression-based slope calculation
- Volatility measurement
- Change percentage calculation

### 5. Automated Insight Generation
- Human-readable insights from analysis results
- Highlights significant findings
- Summarizes key patterns and anomalies

## Installation

The module requires NumPy, which is already included in the project's `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from ny_analysis import NYDataAnalyzer, create_sample_ny_data

# Create sample data
data = create_sample_ny_data()

# Initialize analyzer
analyzer = NYDataAnalyzer(data)

# Perform deep analysis
results = analyzer.deep_analysis()

# View insights
for insight in results['insights']:
    print(insight)
```

### Custom Data Analysis

```python
from ny_analysis import NYDataAnalyzer

# Your custom data
data = [
    {"borough": "Manhattan", "population": 1628706, "median_income": 85000},
    {"borough": "Brooklyn", "population": 2559903, "median_income": 63000},
    # ... more records
]

analyzer = NYDataAnalyzer(data)
stats = analyzer.get_basic_statistics()
print(stats)
```

## API Reference

### Class: NYDataAnalyzer

#### Constructor
```python
NYDataAnalyzer(data: Optional[List[Dict[str, Any]]] = None)
```
Initialize the analyzer with optional data.

#### Methods

##### `load_data(data: List[Dict[str, Any]]) -> None`
Load new data into the analyzer.

##### `add_record(record: Dict[str, Any]) -> None`
Add a single record to the dataset.

##### `get_basic_statistics() -> Dict[str, Any]`
Calculate comprehensive statistics for all fields in the dataset.

**Returns:**
```python
{
    "total_records": int,
    "fields": List[str],
    "numeric_fields": {
        "field_name": {
            "count": int,
            "mean": float,
            "median": float,
            "std": float,
            "min": float,
            "max": float,
            "q25": float,
            "q75": float
        }
    },
    "categorical_fields": {
        "field_name": {
            "unique_count": int,
            "values": List[str],
            "most_common": List[Dict]
        }
    }
}
```

##### `detect_outliers(field: str, method: str = "iqr") -> Dict[str, Any]`
Detect outliers in a numeric field.

**Parameters:**
- `field`: Name of the field to analyze
- `method`: "iqr" (default) or "zscore"

**Returns:**
```python
{
    "field": str,
    "method": str,
    "outlier_count": int,
    "outliers": List[float],
    "outlier_percentage": float
}
```

##### `correlation_analysis(field1: str, field2: str) -> Dict[str, Any]`
Calculate correlation between two numeric fields.

**Returns:**
```python
{
    "field1": str,
    "field2": str,
    "correlation": float,
    "strength": str,  # "strong", "moderate", "weak", or "none"
    "direction": str,  # "positive" or "negative"
    "sample_size": int
}
```

##### `trend_analysis(field: str, time_field: str = "timestamp") -> Dict[str, Any]`
Analyze trends in a numeric field over time.

**Returns:**
```python
{
    "field": str,
    "trend": str,  # "increasing", "decreasing", or "stable"
    "slope": float,
    "volatility": float,
    "start_value": float,
    "end_value": float,
    "change_percentage": float,
    "data_points": int
}
```

##### `deep_analysis() -> Dict[str, Any]`
Perform comprehensive analysis including all available methods.

**Returns:**
```python
{
    "analysis_results": Dict[str, Any],
    "insights": List[str],
    "summary": {
        "total_analyses": int,
        "total_insights": int,
        "timestamp": str
    }
}
```

##### `generate_insights() -> List[str]`
Generate human-readable insights from analysis results.

##### `export_results(filename: str = "analysis_results.json") -> str`
Export analysis results to a JSON file.

### Function: create_sample_ny_data()

Creates sample New York data for demonstration purposes.

**Returns:**
- List of 100 dictionaries with fields: id, borough, category, value, cost, rating, timestamp

## Examples

See `ny_analysis_example.py` for comprehensive examples including:

1. **Basic Statistical Analysis** - Calculate statistics for all fields
2. **Outlier Detection** - Identify anomalous values
3. **Correlation Analysis** - Find relationships between variables
4. **Trend Analysis** - Detect patterns over time
5. **Comprehensive Analysis** - Run all analyses at once
6. **Custom Data** - Use your own datasets

### Running Examples

```bash
python ny_analysis.py           # Run basic demo
python ny_analysis_example.py   # Run all examples
```

## Data Format

The analyzer expects data in the following format:

```python
[
    {
        "field1": value1,
        "field2": value2,
        # ... more fields
    },
    # ... more records
]
```

- Each record is a dictionary
- Fields can be numeric or categorical
- Missing values are handled automatically
- Time fields should be sortable strings (e.g., ISO format)

## Output Files

The module can generate the following output files:

- `ny_analysis_results.json` - Complete analysis results
- `nyc_borough_analysis.json` - Custom analysis results

These JSON files contain:
- All analysis results
- Generated insights
- Data summary and metadata

## Use Cases

### 1. Urban Planning
Analyze demographic, economic, and infrastructure data across NYC boroughs.

### 2. Real Estate Analysis
Study housing prices, rental rates, and market trends.

### 3. Transportation Studies
Evaluate traffic patterns, commute times, and transit efficiency.

### 4. Healthcare Analytics
Examine health metrics, facility distribution, and service accessibility.

### 5. Education Research
Analyze school performance, enrollment trends, and resource allocation.

## Technical Details

### Statistical Methods

- **Mean/Median**: Central tendency measures
- **Standard Deviation**: Variability measurement
- **Quartiles**: Distribution analysis
- **IQR Outliers**: Q1 - 1.5×IQR to Q3 + 1.5×IQR
- **Z-Score Outliers**: |z| > 3 threshold
- **Pearson Correlation**: Linear relationship strength
- **Linear Regression**: Trend slope calculation

### Performance

- Efficient NumPy-based calculations
- Handles datasets up to 100,000+ records
- O(n log n) complexity for most operations

## Limitations

- Designed for structured tabular data
- Requires numeric values for statistical analysis
- Time-series analysis assumes chronological ordering
- Correlation assumes linear relationships

## Future Enhancements

Potential additions for future versions:

- Data visualization (matplotlib/plotly integration)
- More advanced statistical tests
- Machine learning predictions
- Geographic visualization for NY data
- Real-time data streaming analysis
- Database integration (SQL/NoSQL)

## License

Part of the Thalos Prime AI Interface Collection project.

## Support

For questions or issues, please refer to the main project documentation or create an issue in the repository.

## Version History

- **v1.0** (2024) - Initial release
  - Basic statistics
  - Outlier detection
  - Correlation analysis
  - Trend analysis
  - Insight generation
