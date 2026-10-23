
from app.models import CredibilityReport, SourceEvidence
from app.services.ai_analyzer import analyze_content
from app.services.source_verifier import verify_sources


async def generate_report(
    text: str,
    headline: str = "",
    source_url: str = "",
) -> CredibilityReport:
    report = await analyze_content(
        text=text,
        headline=headline,
        source_url=source_url,
    )

    verification = await verify_sources(
        [claim.claim for claim in report.claims]
    )

    # Attach retrieved sources as related sources only.
    # Search results alone do not establish factual support.
    results_by_claim = verification.get("results_by_claim", {})

    for claim in report.claims:
        raw_sources = results_by_claim.get(claim.claim, [])

        for source in raw_sources:
            try:
                claim.related_sources.append(
                    SourceEvidence(
                        title=source["title"],
                        publisher=source["publisher"],
                        url=source["url"],
                        publication_date=source.get(
                            "publication_date"
                        ),
                        finding=source["finding"],
                        relevance=source.get("relevance", ""),
                    )
                )
            except (KeyError, TypeError, ValueError):
                # Ignore malformed search results instead of
                # manufacturing source information.
                continue

    message = verification["message"]

    if message not in report.limitations:
        report.limitations.append(message)

    # Keep the overall assessment conservative until evidence
    # is evaluated and corroborated.
    report.overall_assessment = (
        report.overall_assessment.__class__.INSUFFICIENT_EVIDENCE
    )

    for claim in report.claims:
        claim.assessment = (
            claim.assessment.__class__.UNVERIFIED
        )

        claim.supporting_sources = []
        claim.contradicting_sources = []

    report.evidence_quality = (
        report.evidence_quality.__class__.NONE
    )

    return report
