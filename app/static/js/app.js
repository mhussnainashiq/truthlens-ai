
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analysis-form");
    const textArea = document.getElementById("text");
    const charCount = document.getElementById("char-count");
    const analyzeButton = document.getElementById("analyze-button");
    const clearButton = document.getElementById("clear-button");
    const loadingMessage = document.getElementById("loading-message");

    function updateCharacterCount() {
        if (!textArea || !charCount) return;

        charCount.textContent =
            `${textArea.value.length.toLocaleString()} / 15,000`;
    }

    if (textArea) {
        textArea.addEventListener("input", updateCharacterCount);
        updateCharacterCount();
    }

    document.querySelectorAll("[data-example]").forEach((button) => {
        button.addEventListener("click", () => {
            if (!textArea) return;

            textArea.value = button.dataset.example || "";
            updateCharacterCount();
            textArea.focus();
        });
    });

    if (clearButton) {
        clearButton.addEventListener("click", () => {
            window.setTimeout(() => {
                updateCharacterCount();

                const headline = document.getElementById("headline");
                const sourceUrl = document.getElementById("source_url");

                if (headline) headline.value = "";
                if (sourceUrl) sourceUrl.value = "";
            }, 0);
        });
    }

    if (form) {
        form.addEventListener("submit", (event) => {
            if (!form.checkValidity()) {
                return;
            }

            if (textArea && !textArea.value.trim()) {
                event.preventDefault();
                textArea.focus();
                return;
            }

            if (analyzeButton) {
                analyzeButton.disabled = true;
                analyzeButton.textContent = "Analyzing...";
            }

            if (loadingMessage) {
                loadingMessage.hidden = false;
            }
        });
    }

    const reportField = document.getElementById("report-json");
    const exportStatus = document.getElementById("export-status");

    function getReport() {
        if (!reportField) return null;

        try {
            return JSON.parse(reportField.value);
        } catch {
            if (exportStatus) {
                exportStatus.textContent =
                    "The report could not be prepared for export.";
            }
            return null;
        }
    }

    function reportToText(report) {
        const lines = [
            "TRUTHLENS AI — CREDIBILITY REPORT",
            "",
            `Overall assessment: ${report.overall_assessment}`,
            `Evidence quality: ${report.evidence_quality}`,
            `Demo mode: ${report.demo_mode ? "Yes" : "No"}`,
            "",
            "SUMMARY",
            report.summary,
            "",
            "CLAIMS",
        ];

        (report.claims || []).forEach((claim, index) => {
            lines.push(
                "",
                `${index + 1}. ${claim.claim}`,
                `Assessment: ${claim.assessment}`,
                `Explanation: ${claim.explanation}`,
                "Missing evidence:",
                ...(claim.missing_evidence || []).map(
                    (item) => `- ${item}`
                )
            );

            for (const [label, key] of [
                ["Supporting sources", "supporting_sources"],
                ["Contradicting sources", "contradicting_sources"],
            ]) {
                lines.push(`${label}:`);

                const sources = claim[key] || [];

                if (!sources.length) {
                    lines.push("- None independently retrieved.");
                }

                sources.forEach((source) => {
                    lines.push(
                        `- ${source.title} (${source.publisher})`,
                        `  ${source.url}`,
                        `  ${source.finding}`
                    );
                });
            }
        });

        lines.push(
            "",
            "BIAS ANALYSIS",
            `Level: ${report.bias_analysis?.level || "Unknown"}`,
            report.bias_analysis?.explanation || "",
            "",
            "BIAS INDICATORS",
            ...(report.bias_analysis?.indicators || []).map(
                (item) => `- ${item}`
            ),
            "",
            "RED FLAGS",
            ...(report.red_flags || []).map((item) => `- ${item}`),
            "",
            "RECOMMENDED CHECKS",
            ...(report.recommended_checks || []).map(
                (item) => `- ${item}`
            ),
            "",
            "LIMITATIONS",
            ...(report.limitations || []).map((item) => `- ${item}`),
            "",
            "This report is an AI-assisted assessment, not proof of truth or falsity."
        );

        return lines.join("\n");
    }

    function downloadFile(content, filename, type) {
        const blob = new Blob([content], { type });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();

        window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    const copyButton = document.getElementById("copy-report");
    const txtButton = document.getElementById("download-txt");
    const jsonButton = document.getElementById("download-json");

    if (copyButton) {
        copyButton.addEventListener("click", async () => {
            const report = getReport();
            if (!report) return;

            try {
                await navigator.clipboard.writeText(reportToText(report));

                if (exportStatus) {
                    exportStatus.textContent = "Report copied successfully.";
                }
            } catch {
                if (exportStatus) {
                    exportStatus.textContent =
                        "Copy failed. Try opening the site on localhost or use Download TXT.";
                }
            }
        });
    }

    if (txtButton) {
        txtButton.addEventListener("click", () => {
            const report = getReport();
            if (!report) return;

            downloadFile(
                reportToText(report),
                "truthlens-report.txt",
                "text/plain;charset=utf-8"
            );
        });
    }

    if (jsonButton) {
        jsonButton.addEventListener("click", () => {
            const report = getReport();
            if (!report) return;

            downloadFile(
                JSON.stringify(report, null, 2),
                "truthlens-report.json",
                "application/json;charset=utf-8"
            );
        });
    }
});

