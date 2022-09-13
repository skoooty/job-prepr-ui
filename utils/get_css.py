def get_css():
    return """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://storage.cloud.google.com/job-prepr/Logo.png);
                background-size: 300px 300px;
                background-repeat: no-repeat;
                padding-top: 60px;
                background-position: 20px -70px;
            }
            [data-testid="stSidebarNav"]::after {
                content: "Signed in as:";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 20px;
                position: relative;
                top: 20px;
            }
            [class="css-1pd56a0 e1tzin5v0"] {
                padding-top: 40px;
            }
            [class="css-40ynm6 e1fqkh3o8"] {
                display: none;
            }
            [class="MuiBox-root css-gg4vpm"] {
                visibility: hidden;
            }
            [class="css-1r6slb0 e1tzin5v2"] {
                justify-content: center !important;
                position: bottom !important;
            }
            .css-12oz5g7 {
                flex: 1 1 0%;
                width: 100%;
                padding: 2rem 1rem 10rem;
                max-width: 46rem;
            }
            @font-face {
            font-family: 'Metropolis';
            font-style: normal;
            font-weight: 400;
            src: url(https://storage.cloud.google.com/job-prepr/Metropolis-ExtraLight.otf) format('otf');
            unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
            }

            html, body, [class*="css"]  {
            font-family: 'Metropolis';
            }
        </style>
        """
