#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THALOS PRIME SBI - COMPLETE DATABASE SCHEMA & INITIALIZATION
Copyright © 2026 THALOS PRIME SYSTEMS - Tony Ray Macier III

This file contains all database schemas, initialization scripts, and data management
for the THALOS Prime Synthetic Biological Intelligence system.
"""

import sqlite3
from pathlib import Path


class ThalosDatabaseSchema:
    """Complete database schema for THALOS Prime SBI"""

    # ═══════════════════════════════════════════════════════════════════════════
    # CORE TABLES
    # ═══════════════════════════════════════════════════════════════════════════

    TABLES = {
        "system_config": """
            CREATE TABLE IF NOT EXISTS system_config (
                config_id TEXT PRIMARY KEY,
                parameter_name TEXT UNIQUE NOT NULL,
                parameter_value TEXT NOT NULL,
                parameter_type TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                encrypted BOOLEAN DEFAULT 0
            )
        """,
        "sessions": """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_agent TEXT,
                ip_address TEXT,
                session_status TEXT DEFAULT 'active',
                metadata JSON,
                total_interactions INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0
            )
        """,
        "interactions": """
            CREATE TABLE IF NOT EXISTS interactions (
                interaction_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                query TEXT NOT NULL,
                query_tokens INTEGER,
                response TEXT NOT NULL,
                response_tokens INTEGER,
                intent TEXT,
                confidence REAL,
                response_type TEXT,
                latency_ms INTEGER,
                quality_score REAL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """,
        "context_memory": """
            CREATE TABLE IF NOT EXISTS context_memory (
                memory_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                interaction_index INTEGER,
                context_window TEXT,
                compressed_context BLOB,
                memory_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """,
        "model_parameters": """
            CREATE TABLE IF NOT EXISTS model_parameters (
                param_id TEXT PRIMARY KEY,
                layer_index INTEGER NOT NULL,
                param_type TEXT NOT NULL,
                shape JSON NOT NULL,
                parameter_count INTEGER,
                encrypted_data BLOB,
                parameter_hash TEXT,
                encryption_nonce TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version INTEGER DEFAULT 1
            )
        """,
        "embedding_cache": """
            CREATE TABLE IF NOT EXISTS embedding_cache (
                embedding_id TEXT PRIMARY KEY,
                token_id INTEGER,
                embedding_data BLOB NOT NULL,
                dimension INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP
            )
        """,
        "reasoning_traces": """
            CREATE TABLE IF NOT EXISTS reasoning_traces (
                trace_id TEXT PRIMARY KEY,
                interaction_id TEXT NOT NULL,
                stage INTEGER,
                stage_name TEXT,
                input_data JSON,
                output_data JSON,
                processing_time_ms INTEGER,
                confidence_score REAL,
                FOREIGN KEY (interaction_id) REFERENCES interactions(interaction_id)
            )
        """,
        "confidence_scores": """
            CREATE TABLE IF NOT EXISTS confidence_scores (
                score_id TEXT PRIMARY KEY,
                interaction_id TEXT NOT NULL,
                intent_confidence REAL,
                semantic_confidence REAL,
                overall_confidence REAL,
                quality_rating INTEGER,
                quality_metrics JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (interaction_id) REFERENCES interactions(interaction_id)
            )
        """,
        "encryption_keys": """
            CREATE TABLE IF NOT EXISTS encryption_keys (
                key_id TEXT PRIMARY KEY,
                session_id TEXT,
                key_type TEXT,
                key_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                key_expired_at TIMESTAMP,
                key_iterations INTEGER,
                salt_hash TEXT,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """,
        "security_log": """
            CREATE TABLE IF NOT EXISTS security_log (
                log_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                severity TEXT,
                description TEXT,
                session_id TEXT,
                ip_address TEXT,
                metadata JSON,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """,
        "model_version_history": """
            CREATE TABLE IF NOT EXISTS model_version_history (
                version_id TEXT PRIMARY KEY,
                version_number INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                parameter_count INTEGER,
                performance_metrics JSON,
                deployed BOOLEAN DEFAULT 0,
                description TEXT
            )
        """,
        "intent_patterns": """
            CREATE TABLE IF NOT EXISTS intent_patterns (
                pattern_id TEXT PRIMARY KEY,
                intent_name TEXT,
                keywords TEXT,
                confidence_threshold REAL,
                response_template TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "semantic_mappings": """
            CREATE TABLE IF NOT EXISTS semantic_mappings (
                mapping_id TEXT PRIMARY KEY,
                input_text TEXT,
                semantic_vector BLOB,
                intent TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "performance_metrics": """
            CREATE TABLE IF NOT EXISTS performance_metrics (
                metric_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                avg_latency_ms REAL,
                max_latency_ms INTEGER,
                min_latency_ms INTEGER,
                requests_per_second REAL,
                average_confidence REAL,
                memory_usage_mb INTEGER,
                cpu_usage_percent REAL
            )
        """,
        "audit_log": """
            CREATE TABLE IF NOT EXISTS audit_log (
                audit_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                action_type TEXT,
                actor_session_id TEXT,
                target_resource TEXT,
                changes_json JSON,
                result TEXT,
                FOREIGN KEY (actor_session_id) REFERENCES sessions(session_id)
            )
        """,
        "feature_flags": """
            CREATE TABLE IF NOT EXISTS feature_flags (
                flag_id TEXT PRIMARY KEY,
                flag_name TEXT UNIQUE NOT NULL,
                is_enabled BOOLEAN DEFAULT 1,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "error_log": """
            CREATE TABLE IF NOT EXISTS error_log (
                error_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_type TEXT,
                error_message TEXT,
                stack_trace TEXT,
                session_id TEXT,
                interaction_id TEXT,
                severity TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                FOREIGN KEY (interaction_id) REFERENCES interactions(interaction_id)
            )
        """,
    }

    # ═══════════════════════════════════════════════════════════════════════════
    # INDEXES FOR PERFORMANCE
    # ═══════════════════════════════════════════════════════════════════════════

    INDEXES = {
        "idx_session_id": "CREATE INDEX IF NOT EXISTS idx_session_id ON interactions(session_id)",
        "idx_timestamp": "CREATE INDEX IF NOT EXISTS idx_timestamp ON interactions(timestamp)",
        "idx_intent": "CREATE INDEX IF NOT EXISTS idx_intent ON interactions(intent)",
        "idx_confidence": "CREATE INDEX IF NOT EXISTS idx_confidence ON confidence_scores(overall_confidence)",
        "idx_layer_index": "CREATE INDEX IF NOT EXISTS idx_layer_index ON model_parameters(layer_index)",
        "idx_security_log_timestamp": "CREATE INDEX IF NOT EXISTS idx_security_log_timestamp ON security_log(timestamp)",
        "idx_audit_log_action": "CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action_type)",
    }

    # ═══════════════════════════════════════════════════════════════════════════
    # VIEWS FOR COMMON QUERIES
    # ═══════════════════════════════════════════════════════════════════════════

    VIEWS = {
        "vw_session_summary": """
            CREATE VIEW IF NOT EXISTS vw_session_summary AS
            SELECT 
                s.session_id,
                s.created_at,
                s.last_activity,
                COUNT(i.interaction_id) as total_interactions,
                AVG(i.confidence) as avg_confidence,
                MAX(i.timestamp) as last_query_time,
                SUM(i.query_tokens + i.response_tokens) as total_tokens
            FROM sessions s
            LEFT JOIN interactions i ON s.session_id = i.session_id
            GROUP BY s.session_id
        """,
        "vw_interaction_details": """
            CREATE VIEW IF NOT EXISTS vw_interaction_details AS
            SELECT 
                i.interaction_id,
                i.session_id,
                i.timestamp,
                i.intent,
                i.confidence,
                i.latency_ms,
                COUNT(rt.trace_id) as reasoning_stages,
                AVG(cs.overall_confidence) as avg_quality
            FROM interactions i
            LEFT JOIN reasoning_traces rt ON i.interaction_id = rt.interaction_id
            LEFT JOIN confidence_scores cs ON i.interaction_id = cs.interaction_id
            GROUP BY i.interaction_id
        """,
        "vw_model_statistics": """
            CREATE VIEW IF NOT EXISTS vw_model_statistics AS
            SELECT 
                COUNT(DISTINCT param_id) as total_parameters,
                COUNT(DISTINCT layer_index) as total_layers,
                SUM(parameter_count) as total_param_count,
                MAX(version) as latest_version
            FROM model_parameters
        """,
    }


def initialize_thalos_database(db_path: Path):
    """Initialize complete THALOS Prime database"""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    print("\n[DATABASE] Initializing THALOS Prime database schema...")

    # Create tables
    for table_name, schema in ThalosDatabaseSchema.TABLES.items():
        print(f"  ├─ Creating table: {table_name}")
        cursor.execute(schema)

    # Create indexes
    for index_name, index_sql in ThalosDatabaseSchema.INDEXES.items():
        print(f"  ├─ Creating index: {index_name}")
        cursor.execute(index_sql)

    # Create views
    for view_name, view_sql in ThalosDatabaseSchema.VIEWS.items():
        print(f"  ├─ Creating view: {view_name}")
        cursor.execute(view_sql)

    # Initialize system configuration
    print("  └─ Initializing system configuration")
    initialize_system_config(cursor)

    conn.commit()
    conn.close()

    print("[SUCCESS] Database initialization complete\n")


def initialize_system_config(cursor):
    """Initialize system configuration parameters"""

    config_params = {
        "system_name": ("string", "THALOS PRIME SBI"),
        "version": ("string", "6.0"),
        "build_date": ("string", "2026-02-05"),
        "creator": ("string", "Tony Ray Macier III"),
        "company": ("string", "THALOS PRIME SYSTEMS"),
        "vocab_size": ("integer", "50257"),
        "embedding_dimension": ("integer", "768"),
        "hidden_dimension": ("integer", "3072"),
        "num_heads": ("integer", "12"),
        "num_layers": ("integer", "24"),
        "total_parameters": ("integer", "200000000"),
        "context_memory_size": ("integer", "100"),
        "reasoning_depth": ("integer", "5"),
        "encryption_algorithm": ("string", "AES-256-GCM"),
        "hash_algorithm": ("string", "SHA-3-512"),
        "enable_reasoning_trace": ("boolean", "1"),
        "enable_confidence_scoring": ("boolean", "1"),
        "enable_context_compression": ("boolean", "1"),
        "enable_adaptive_temperature": ("boolean", "1"),
    }

    import secrets

    for param_name, (param_type, param_value) in config_params.items():
        config_id = "cfg_" + secrets.token_hex(8)
        cursor.execute(
            """
            INSERT INTO system_config 
            (config_id, parameter_name, parameter_value, parameter_type, description)
            VALUES (?, ?, ?, ?, ?)
        """,
            (config_id, param_name, param_value, param_type, f"System parameter: {param_name}"),
        )


if __name__ == "__main__":
    db_path = Path.home() / "THALOS_PRIME_SBI" / "data" / "thalos_prime.db"
    initialize_thalos_database(db_path)
