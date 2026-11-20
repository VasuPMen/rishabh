using { cuid, managed } from '@sap/cds/common';

service BillingReviewService @(path: '/api') {

    // ── Chat with the agent ────────────────────────────────────────────────
    action chat(
        message      : String not null,
        history      : array of {
            role    : String;
            content : String;
        },
        customer_id  : String,
        customer_name: String
    ) returns {
        response : String;
        history  : array of {
            role    : String;
            content : String;
        };
    };

    // ── List available customers ───────────────────────────────────────────
    function customers() returns array of {
        id   : String;
        name : String;
    };

    // ── Health check ───────────────────────────────────────────────────────
    function health() returns {
        status  : String;
        service : String;
    };
}
