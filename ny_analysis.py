"""
Deep Analysis Module for NY (New York) Data
============================================

This module provides comprehensive data analysis capabilities for datasets,
with a focus on New York data analysis. It includes statistical analysis,
data visualization, and insight generation.

Author: Thalos Prime AI System
Version: 1.0
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
import json


class NYDataAnalyzer:
    """
    Advanced data analyzer for New York datasets with deep statistical
    analysis and insight generation capabilities.
    """
    
    def __init__(self, data: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the analyzer with optional data.
        
        Args:
            data: List of dictionaries containing the dataset to analyze
        """
        self.data = data or []
        self.analysis_results = {}
        self.insights = []
        
    def load_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Load data into the analyzer.
        
        Args:
            data: List of dictionaries containing the dataset
        """
        self.data = data
        self.analysis_results = {}
        self.insights = []
        
    def add_record(self, record: Dict[str, Any]) -> None:
        """
        Add a single record to the dataset.
        
        Args:
            record: Dictionary containing a single data record
        """
        self.data.append(record)
        
    def get_basic_statistics(self) -> Dict[str, Any]:
        """
        Calculate basic statistics for the dataset.
        
        Returns:
            Dictionary containing basic statistical measures
        """
        if not self.data:
            return {"error": "No data available for analysis"}
            
        stats = {
            "total_records": len(self.data),
            "timestamp": datetime.now().isoformat(),
            "fields": list(self.data[0].keys()) if self.data else [],
            "numeric_fields": {},
            "categorical_fields": {}
        }
        
        # Analyze each field
        if self.data:
            fields = self.data[0].keys()
            for field in fields:
                values = [record.get(field) for record in self.data if field in record]
                
                # Check if numeric
                try:
                    numeric_values = [float(v) for v in values if v is not None]
                    if numeric_values:
                        stats["numeric_fields"][field] = {
                            "count": len(numeric_values),
                            "mean": np.mean(numeric_values),
                            "median": np.median(numeric_values),
                            "std": np.std(numeric_values),
                            "min": np.min(numeric_values),
                            "max": np.max(numeric_values),
                            "q25": np.percentile(numeric_values, 25),
                            "q75": np.percentile(numeric_values, 75)
                        }
                except (ValueError, TypeError):
                    # Categorical field
                    unique_values = list(set(str(v) for v in values if v is not None))
                    stats["categorical_fields"][field] = {
                        "unique_count": len(unique_values),
                        "values": unique_values[:10],  # First 10 unique values
                        "most_common": self._find_most_common(values)
                    }
                    
        self.analysis_results["basic_statistics"] = stats
        return stats
        
    def _find_most_common(self, values: List[Any], top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Find the most common values in a list.
        
        Args:
            values: List of values to analyze
            top_n: Number of top values to return
            
        Returns:
            List of dictionaries with value and count
        """
        from collections import Counter
        counter = Counter(str(v) for v in values if v is not None)
        return [{"value": v, "count": c} for v, c in counter.most_common(top_n)]
        
    def detect_outliers(self, field: str, method: str = "iqr") -> Dict[str, Any]:
        """
        Detect outliers in a numeric field using specified method.
        
        Args:
            field: Name of the field to analyze
            method: Method to use ('iqr' or 'zscore')
            
        Returns:
            Dictionary containing outlier information
        """
        if not self.data:
            return {"error": "No data available"}
            
        try:
            values = [float(record.get(field)) for record in self.data 
                     if field in record and record.get(field) is not None]
            
            if not values:
                return {"error": f"No numeric values found for field '{field}'"}
                
            outliers = []
            
            if method == "iqr":
                q25 = np.percentile(values, 25)
                q75 = np.percentile(values, 75)
                iqr = q75 - q25
                lower_bound = q25 - 1.5 * iqr
                upper_bound = q75 + 1.5 * iqr
                outliers = [v for v in values if v < lower_bound or v > upper_bound]
                
            elif method == "zscore":
                mean = np.mean(values)
                std = np.std(values)
                z_scores = [(v - mean) / std if std > 0 else 0 for v in values]
                outliers = [v for v, z in zip(values, z_scores) if abs(z) > 3]
                
            result = {
                "field": field,
                "method": method,
                "outlier_count": len(outliers),
                "outliers": outliers[:20],  # First 20 outliers
                "outlier_percentage": (len(outliers) / len(values)) * 100 if values else 0
            }
            
            self.analysis_results[f"outliers_{field}"] = result
            return result
            
        except (ValueError, TypeError) as e:
            return {"error": f"Error detecting outliers: {str(e)}"}
            
    def correlation_analysis(self, field1: str, field2: str) -> Dict[str, Any]:
        """
        Calculate correlation between two numeric fields.
        
        Args:
            field1: First field name
            field2: Second field name
            
        Returns:
            Dictionary containing correlation information
        """
        if not self.data:
            return {"error": "No data available"}
            
        try:
            values1 = []
            values2 = []
            
            for record in self.data:
                if field1 in record and field2 in record:
                    v1 = record.get(field1)
                    v2 = record.get(field2)
                    if v1 is not None and v2 is not None:
                        values1.append(float(v1))
                        values2.append(float(v2))
                        
            if len(values1) < 2:
                return {"error": "Insufficient data for correlation analysis"}
                
            correlation = np.corrcoef(values1, values2)[0, 1]
            
            # Interpret correlation strength
            strength = "none"
            if abs(correlation) > 0.7:
                strength = "strong"
            elif abs(correlation) > 0.4:
                strength = "moderate"
            elif abs(correlation) > 0.1:
                strength = "weak"
                
            result = {
                "field1": field1,
                "field2": field2,
                "correlation": float(correlation),
                "strength": strength,
                "direction": "positive" if correlation > 0 else "negative",
                "sample_size": len(values1)
            }
            
            self.analysis_results[f"correlation_{field1}_{field2}"] = result
            return result
            
        except (ValueError, TypeError) as e:
            return {"error": f"Error calculating correlation: {str(e)}"}
            
    def trend_analysis(self, field: str, time_field: str = "timestamp") -> Dict[str, Any]:
        """
        Analyze trends in a numeric field over time.
        
        Args:
            field: Name of the field to analyze
            time_field: Name of the time/date field
            
        Returns:
            Dictionary containing trend information
        """
        if not self.data:
            return {"error": "No data available"}
            
        try:
            sorted_data = sorted(
                [r for r in self.data if field in r and time_field in r],
                key=lambda x: x.get(time_field, "")
            )
            
            values = [float(record.get(field)) for record in sorted_data 
                     if record.get(field) is not None]
            
            if len(values) < 2:
                return {"error": "Insufficient data for trend analysis"}
                
            # Calculate trend using linear regression
            x = np.arange(len(values))
            coefficients = np.polyfit(x, values, 1)
            slope = coefficients[0]
            
            # Determine trend direction
            trend = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
            
            # Calculate volatility
            volatility = np.std(values) / np.mean(values) if np.mean(values) != 0 else 0
            
            result = {
                "field": field,
                "trend": trend,
                "slope": float(slope),
                "volatility": float(volatility),
                "start_value": float(values[0]),
                "end_value": float(values[-1]),
                "change_percentage": ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0,
                "data_points": len(values)
            }
            
            self.analysis_results[f"trend_{field}"] = result
            return result
            
        except (ValueError, TypeError, IndexError) as e:
            return {"error": f"Error analyzing trends: {str(e)}"}
            
    def generate_insights(self) -> List[str]:
        """
        Generate human-readable insights from the analysis results.
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Insights from basic statistics
        if "basic_statistics" in self.analysis_results:
            stats = self.analysis_results["basic_statistics"]
            insights.append(f"Dataset contains {stats['total_records']} records")
            
            if stats.get("numeric_fields"):
                insights.append(f"Found {len(stats['numeric_fields'])} numeric fields for analysis")
                
            if stats.get("categorical_fields"):
                insights.append(f"Found {len(stats['categorical_fields'])} categorical fields")
                
        # Insights from outliers
        for key, value in self.analysis_results.items():
            if key.startswith("outliers_") and not value.get("error"):
                if value["outlier_count"] > 0:
                    insights.append(
                        f"Detected {value['outlier_count']} outliers in '{value['field']}' "
                        f"({value['outlier_percentage']:.1f}% of data)"
                    )
                    
        # Insights from correlations
        for key, value in self.analysis_results.items():
            if key.startswith("correlation_") and not value.get("error"):
                if value["strength"] in ["strong", "moderate"]:
                    insights.append(
                        f"Found {value['strength']} {value['direction']} correlation "
                        f"({value['correlation']:.3f}) between '{value['field1']}' and '{value['field2']}'"
                    )
                    
        # Insights from trends
        for key, value in self.analysis_results.items():
            if key.startswith("trend_") and not value.get("error"):
                insights.append(
                    f"'{value['field']}' shows {value['trend']} trend "
                    f"with {value['change_percentage']:.1f}% change"
                )
                
        self.insights = insights
        return insights
        
    def deep_analysis(self) -> Dict[str, Any]:
        """
        Perform comprehensive deep analysis on the dataset.
        
        Returns:
            Dictionary containing all analysis results and insights
        """
        if not self.data:
            return {"error": "No data available for analysis"}
            
        # Run all analyses
        basic_stats = self.get_basic_statistics()
        
        # Analyze outliers for numeric fields
        if "numeric_fields" in basic_stats:
            for field in basic_stats["numeric_fields"].keys():
                self.detect_outliers(field)
                
        # Perform correlation analysis for pairs of numeric fields
        if "numeric_fields" in basic_stats:
            numeric_fields = list(basic_stats["numeric_fields"].keys())
            for i, field1 in enumerate(numeric_fields):
                for field2 in numeric_fields[i+1:]:
                    self.correlation_analysis(field1, field2)
                    
        # Generate insights
        insights = self.generate_insights()
        
        return {
            "analysis_results": self.analysis_results,
            "insights": insights,
            "summary": {
                "total_analyses": len(self.analysis_results),
                "total_insights": len(insights),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    def export_results(self, filename: str = "analysis_results.json") -> str:
        """
        Export analysis results to a JSON file.
        
        Args:
            filename: Name of the output file
            
        Returns:
            Success message or error
        """
        try:
            results = {
                "analysis_results": self.analysis_results,
                "insights": self.insights,
                "data_summary": {
                    "total_records": len(self.data),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
                
            return f"Results exported successfully to {filename}"
        except Exception as e:
            return f"Error exporting results: {str(e)}"


def create_sample_ny_data() -> List[Dict[str, Any]]:
    """
    Create sample New York data for demonstration purposes.
    
    Returns:
        List of dictionaries containing sample NY data
    """
    np.random.seed(42)
    
    boroughs = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]
    categories = ["Housing", "Transportation", "Education", "Healthcare", "Recreation"]
    
    data = []
    for i in range(100):
        record = {
            "id": i + 1,
            "borough": np.random.choice(boroughs),
            "category": np.random.choice(categories),
            "value": np.random.normal(100, 20),
            "cost": np.random.uniform(50, 500),
            "rating": np.random.uniform(1, 5),
            "timestamp": f"2024-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}"
        }
        data.append(record)
        
    return data


if __name__ == "__main__":
    # Example usage
    print("=" * 80)
    print("NY Data Deep Analysis Module")
    print("=" * 80)
    print()
    
    # Create sample data
    print("Creating sample New York data...")
    sample_data = create_sample_ny_data()
    print(f"Created {len(sample_data)} sample records")
    print()
    
    # Initialize analyzer
    analyzer = NYDataAnalyzer(sample_data)
    
    # Perform deep analysis
    print("Performing deep analysis...")
    results = analyzer.deep_analysis()
    print()
    
    # Display insights
    print("=" * 80)
    print("INSIGHTS:")
    print("=" * 80)
    for i, insight in enumerate(results["insights"], 1):
        print(f"{i}. {insight}")
    print()
    
    # Display summary
    print("=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    summary = results["summary"]
    print(f"Total Analyses Performed: {summary['total_analyses']}")
    print(f"Total Insights Generated: {summary['total_insights']}")
    print(f"Analysis Timestamp: {summary['timestamp']}")
    print()
    
    # Export results
    export_msg = analyzer.export_results("ny_analysis_results.json")
    print(export_msg)
    print()
    print("=" * 80)
