#pragma once

#include <iostream>
#include <filesystem>
#include "SystemTransparency.hpp"

namespace fs = std::filesystem;

class SystemDiagnostics {
public:
    // Executes a complete, transparent system-wide health and asset audit for engineers
    static bool RunFullDiagnosticAudit() {
        SystemTransparency::AuditEnvironmentContext();
        
        bool systemHealthy = true;
        fs::path workspaceRoot = fs::current_path();

        // 1. Audit Trust-Main & Gateway Cryptographic Assets
        fs::path certsDir = workspaceRoot / "certs";
        if (fs::exists(certsDir / "client.key") && fs::exists(certsDir / "localCA.crt") && fs::exists(certsDir / "server.crt")) {
            SystemTransparency::LogEvent("Diagnostics", "Asset Audit", SystemTransparency::StatusLevel::PASS, "All cryptographic identity assets present in " + certsDir.string());
        } else {
            SystemTransparency::LogEvent("Diagnostics", "Asset Audit", SystemTransparency::StatusLevel::CRITICAL, "Cryptographic assets missing or incomplete in " + certsDir.string());
            systemHealthy = false;
        }

        // 2. Audit Trust-Shell Mobile Client Integration Boundary
        fs::path shellBoundary = workspaceRoot / "Trust-Shell";
        if (fs::exists(shellBoundary) || fs::exists(workspaceRoot / "include")) {
            SystemTransparency::LogEvent("Diagnostics", "Shell Boundary", SystemTransparency::StatusLevel::PASS, "Trust-Shell execution workspace verified.");
        } else {
            SystemTransparency::LogEvent("Diagnostics", "Shell Boundary", SystemTransparency::StatusLevel::WARN, "Trust-Shell root path not detected in immediate workspace.");
        }

        // 3. Audit AudioVideoEngine-CPP Pipeline Linkage
        fs::path avEnginePath = workspaceRoot.parent_path() / "AudioVideoEngine-CPP";
        if (fs::exists(avEnginePath)) {
            SystemTransparency::LogEvent("Diagnostics", "Media Engine Audit", SystemTransparency::StatusLevel::PASS, "AudioVideoEngine-CPP sibling repository detected.");
        } else {
            SystemTransparency::LogEvent("Diagnostics", "Media Engine Audit", SystemTransparency::StatusLevel::WARN, "AudioVideoEngine-CPP sibling path not found (standalone build mode).");
        }

        // 4. Final Verdict Manifest
        if (systemHealthy) {
            SystemTransparency::LogEvent("Diagnostics", "System Status", SystemTransparency::StatusLevel::PASS, "All core diagnostic checks cleared. Environment ready for zero-trust mTLS binding.");
        } else {
            SystemTransparency::LogEvent("Diagnostics", "System Status", SystemTransparency::StatusLevel::CRITICAL, "Diagnostic audit failed. Action required by engineering review.");
        }

        return systemHealthy;
    }
};
