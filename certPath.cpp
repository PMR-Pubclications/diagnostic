#include <filesystem>
#include <fstream>
#include <iostream>
#ifndef _WIN32
#include <sys/stat.h>
#endif

namespace fs = std::filesystem;

class TrustDiagnostics {
public:
    static bool AuditIdentityPipeline(const fs::path& caPath, const fs::path& certPath, const fs::path& keyPath) {
        bool allGood = true;
        std::cout << "[Diagnostics] Auditing mTLS Identity Pipeline..." << std::endl;

        // 1. Check Root CA
        if (fs::exists(caPath)) {
            std::cout << "  [OK] Root CA found: " << caPath << std::endl;
        } else {
            std::cerr << "  [FAIL] Missing Root CA at: " << caPath << std::endl;
            allGood = false;
        }

        // 2. Check Client Certificate
        if (fs::exists(certPath)) {
            std::cout << "  [OK] Client Certificate found: " << certPath << std::endl;
        } else {
            std::cerr << "  [FAIL] Missing Client Certificate at: " << certPath << std::endl;
            allGood = false;
        }

        // 3. Check Private Key & Permissions
        if (fs::exists(keyPath)) {
            std::cout << "  [OK] Private Key found: " << keyPath << std::endl;
            
            #ifndef _WIN32
            // Verify file permissions are locked down (0600)
            struct stat st;
            if (stat(keyPath.string().c_str(), &st) == 0) {
                mode_t perms = st.st_mode & 0777;
                if (perms == 0600) {
                    std::cout << "  [OK] Private key permissions secure (0600)." << std::endl;
                } else {
                    std::cerr << "  [WARN] Private key permissions are too open (" 
                              << std::oct << perms << std::dec << "). Recommended: 0600." << std::endl;
                }
            }
            #endif
        } else {
            std::cerr << "  [FAIL] Missing Private Key at: " << keyPath << std::endl;
            allGood = false;
        }

        return allGood;
    }
};
