"""
Example Usage of NY Data Deep Analysis Module
==============================================

This script demonstrates how to use the ny_analysis module for
comprehensive data analysis.
"""

from ny_analysis import NYDataAnalyzer, create_sample_ny_data
import json


def example_basic_analysis():
    """Example 1: Basic statistical analysis"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Statistical Analysis")
    print("="*80)
    
    # Create sample data
    data = create_sample_ny_data()
    analyzer = NYDataAnalyzer(data)
    
    # Get basic statistics
    stats = analyzer.get_basic_statistics()
    
    print(f"\nTotal Records: {stats['total_records']}")
    print(f"\nNumeric Fields:")
    for field, field_stats in stats['numeric_fields'].items():
        print(f"  {field}:")
        print(f"    Mean: {field_stats['mean']:.2f}")
        print(f"    Std Dev: {field_stats['std']:.2f}")
        print(f"    Range: [{field_stats['min']:.2f}, {field_stats['max']:.2f}]")
        
    print(f"\nCategorical Fields:")
    for field, field_stats in stats['categorical_fields'].items():
        print(f"  {field}: {field_stats['unique_count']} unique values")


def example_outlier_detection():
    """Example 2: Outlier detection"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Outlier Detection")
    print("="*80)
    
    data = create_sample_ny_data()
    analyzer = NYDataAnalyzer(data)
    
    # Detect outliers in value field
    outliers = analyzer.detect_outliers("value", method="iqr")
    
    if not outliers.get("error"):
        print(f"\nField: {outliers['field']}")
        print(f"Method: {outliers['method']}")
        print(f"Outliers Found: {outliers['outlier_count']}")
        print(f"Percentage: {outliers['outlier_percentage']:.2f}%")
        
        if outliers['outlier_count'] > 0:
            print(f"Sample Outliers: {outliers['outliers'][:5]}")


def example_correlation_analysis():
    """Example 3: Correlation analysis"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Correlation Analysis")
    print("="*80)
    
    data = create_sample_ny_data()
    analyzer = NYDataAnalyzer(data)
    
    # Analyze correlation between cost and rating
    correlation = analyzer.correlation_analysis("cost", "rating")
    
    if not correlation.get("error"):
        print(f"\nAnalyzing: {correlation['field1']} vs {correlation['field2']}")
        print(f"Correlation Coefficient: {correlation['correlation']:.4f}")
        print(f"Strength: {correlation['strength']}")
        print(f"Direction: {correlation['direction']}")
        print(f"Sample Size: {correlation['sample_size']}")


def example_trend_analysis():
    """Example 4: Trend analysis"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Trend Analysis")
    print("="*80)
    
    data = create_sample_ny_data()
    analyzer = NYDataAnalyzer(data)
    
    # Analyze trend in value over time
    trend = analyzer.trend_analysis("value", "timestamp")
    
    if not trend.get("error"):
        print(f"\nField: {trend['field']}")
        print(f"Trend: {trend['trend']}")
        print(f"Slope: {trend['slope']:.4f}")
        print(f"Change: {trend['change_percentage']:.2f}%")
        print(f"Volatility: {trend['volatility']:.4f}")
        print(f"Start Value: {trend['start_value']:.2f}")
        print(f"End Value: {trend['end_value']:.2f}")


def example_comprehensive_analysis():
    """Example 5: Comprehensive deep analysis"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Comprehensive Deep Analysis")
    print("="*80)
    
    data = create_sample_ny_data()
    analyzer = NYDataAnalyzer(data)
    
    # Perform full deep analysis
    results = analyzer.deep_analysis()
    
    print(f"\nTotal Analyses: {results['summary']['total_analyses']}")
    print(f"Total Insights: {results['summary']['total_insights']}")
    print(f"\nKey Insights:")
    for i, insight in enumerate(results['insights'][:5], 1):
        print(f"  {i}. {insight}")
        
    if len(results['insights']) > 5:
        print(f"  ... and {len(results['insights']) - 5} more insights")


def example_custom_data():
    """Example 6: Custom data analysis"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Custom Data Analysis")
    print("="*80)
    
    # Create custom dataset
    custom_data = [
        {"borough": "Manhattan", "population": 1628706, "area_sqmi": 23, "median_income": 85000},
        {"borough": "Brooklyn", "population": 2559903, "area_sqmi": 71, "median_income": 63000},
        {"borough": "Queens", "population": 2253858, "area_sqmi": 109, "median_income": 69000},
        {"borough": "Bronx", "population": 1418207, "area_sqmi": 42, "median_income": 40000},
        {"borough": "Staten Island", "population": 476143, "area_sqmi": 58, "median_income": 79000}
    ]
    
    analyzer = NYDataAnalyzer(custom_data)
    
    # Get basic statistics
    stats = analyzer.get_basic_statistics()
    print(f"\nAnalyzing NYC Borough Data:")
    print(f"Total Boroughs: {stats['total_records']}")
    
    # Check correlation between area and population
    correlation = analyzer.correlation_analysis("area_sqmi", "population")
    if not correlation.get("error"):
        print(f"\nArea vs Population Correlation: {correlation['correlation']:.4f}")
        print(f"Strength: {correlation['strength']}")
        
    # Export results
    export_msg = analyzer.export_results("nyc_borough_analysis.json")
    print(f"\n{export_msg}")


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("NY DATA DEEP ANALYSIS - EXAMPLE DEMONSTRATIONS")
    print("="*80)
    
    # Run all examples
    example_basic_analysis()
    example_outlier_detection()
    example_correlation_analysis()
    example_trend_analysis()
    example_comprehensive_analysis()
    example_custom_data()
    
    print("\n" + "="*80)
    print("All examples completed successfully!")
    print("="*80)
    print("\nGenerated Files:")
    print("  - ny_analysis_results.json (from comprehensive analysis)")
    print("  - nyc_borough_analysis.json (from custom data analysis)")
    print("\n")


if __name__ == "__main__":
    main()
