# p65 interference tally: exploratory analyses that respect clustering by paper (2026-11-17, B-1022 pre-upload).
# (1) Ordinal mixed model: direction code as a three-level ordered outcome (time over space < symmetric <
#     space over time), random intercept per paper, symmetric thresholds. The latent distribution is centred at
#     -central.1 on the logit scale (clm parameterises thresholds as central +/- spacing), so central.1 = 0 is the
#     hypothesis that space-over-time and time-over-space are equally likely once paper clustering is absorbed.
#     Package ordinal::clmm, native ARM R.
# (2) Paper-clustered permutation (sign-flip) test of the registered statistic (space-over-time minus
#     time-over-space votes): every experiment in a paper flips direction together, 200,000 Monte Carlo flips.
# Run:
#   env PATH=/opt/homebrew/bin:/usr/bin:/bin R_LIBS_USER=/Users/as/opt/R-arm64-lib /opt/homebrew/bin/Rscript published-asymmetry/p65_clmm_by-paper_2026-11-17.R
suppressPackageStartupMessages(library(ordinal))
args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args)) args[1] else "."
d <- read.delim(file.path(root, "published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv"),
                quote = "", stringsAsFactors = FALSE, check.names = FALSE)
codes <- c("SPACE>TIME", "TIME>SPACE", "SYMMETRIC", "NONE")
d <- d[trimws(d$code) %in% codes & !grepl("CLINICAL", toupper(d$tags)) &
       !startsWith(toupper(d$verification), "SECONDARY"), ]
d$code <- trimws(d$code); stopifnot(nrow(d) == 64)  # 64 before the 2026-11-19 G04 merge (63), 64 again after the 2026-11-19 full-text recode (Riemer et al. 2026 Exp 2 added)
d$paper <- factor(ifelse(nzchar(d$doi), d$doi, d$key))
cat("papers (all 64):", nlevels(d$paper), "\n")
# ---- (1) ordinal mixed model on the 61 experiments with a direction or symmetry (NONE dropped)
o <- d[d$code != "NONE", ]
o$y <- factor(o$code, levels = c("TIME>SPACE", "SYMMETRIC", "SPACE>TIME"), ordered = TRUE)
o$paper <- droplevels(o$paper)
cat("clmm rows:", nrow(o), " papers:", nlevels(o$paper), "\n"); print(table(o$y))
fit <- clmm(y ~ 1 + (1 | paper), data = o, threshold = "symmetric", link = "logit", Hess = TRUE, nAGQ = 7)
s <- summary(fit)
print(s)
V <- vcov(fit); th <- coef(fit)[c("central.1", "central.2")]
# with three categories "symmetric" leaves both thresholds free (central.1, central.2); the latent centre is their
# midpoint, with a delta-method SE
mid <- mean(th); se_mid <- sqrt((V["central.1", "central.1"] + V["central.2", "central.2"] + 2 * V["central.1", "central.2"]) / 4)
z <- mid / se_mid; p_wald <- 2 * pnorm(-abs(z))
cat(sprintf("\nthreshold midpoint: est = %.4f, SE = %.4f, z = %.2f, Wald p = %.4f\n", mid, se_mid, z, p_wald))
cat(sprintf("latent centre = %.3f logits toward space-over-time (minus the midpoint); paper SD = %.3f\n",
            -mid, sqrt(VarCorr(fit)$paper[1, 1])))
cat("convergence code (0 = ok):", fit$optRes$convergence, " | message:", fit$optRes$message, "\n")
# likelihood-ratio test against thresholds symmetric about zero (symmetric2), the model of no lean
fit0 <- clmm(y ~ 1 + (1 | paper), data = o, threshold = "symmetric2", link = "logit", Hess = TRUE, nAGQ = 7)
lr <- 2 * (logLik(fit) - logLik(fit0)); p_lr <- pchisq(as.numeric(lr), 1, lower.tail = FALSE)
cat(sprintf("LR test of centre = 0: G2 = %.3f on 1 df, p = %.4f (null model converged: %d)\n", lr, p_lr, fit0$optRes$convergence))
p_ts <- plogis(th[1]); p_st <- 1 - plogis(th[2])
cat(sprintf("implied at a typical paper: P(time over space) = %.3f, P(symmetric) = %.3f, P(space over time) = %.3f\n",
            p_ts, 1 - p_ts - p_st, p_st))
# controls
set.seed(20261117)
o$y_sh <- factor(sample(as.character(o$y)), levels = levels(o$y), ordered = TRUE)
# control 1: outcome shuffled across experiments (breaks any direction lean? no: shuffling keeps the marginal 26/14,
# so central stays; it breaks the paper clustering, so the paper SD must drop toward 0)
fsh <- clmm(y_sh ~ 1 + (1 | paper), data = o, threshold = "symmetric", link = "logit", Hess = TRUE, nAGQ = 7)
cat(sprintf("control (shuffled across papers): midpoint = %.3f, paper SD = %.3f (clustering removed)\n",
            mean(coef(fsh)[c("central.1", "central.2")]), sqrt(VarCorr(fsh)$paper[1, 1])))
# control 2: mirror the codes (swap time/space): central must change sign
o$y_mir <- factor(c("TIME>SPACE" = "SPACE>TIME", "SYMMETRIC" = "SYMMETRIC", "SPACE>TIME" = "TIME>SPACE")[as.character(o$y)],
                  levels = levels(o$y), ordered = TRUE)
fmir <- clmm(y_mir ~ 1 + (1 | paper), data = o, threshold = "symmetric", link = "logit", Hess = TRUE, nAGQ = 7)
mid_mir <- mean(coef(fmir)[c("central.1", "central.2")])
cat(sprintf("control (mirrored codes): midpoint = %.3f (must be minus the original %.3f)\n", mid_mir, mid))
stopifnot(abs(mid_mir + mid) < 0.02)
# ---- (2) paper-clustered sign-flip permutation of the registered statistic
dir <- d[d$code %in% c("SPACE>TIME", "TIME>SPACE"), ]
dir$s <- ifelse(dir$code == "SPACE>TIME", 1L, -1L)
per_paper <- tapply(dir$s, droplevels(dir$paper), sum)
k <- length(per_paper); obs <- sum(per_paper)
cat(sprintf("\nsign-flip test: %d directional experiments in %d papers, observed S>T minus T>S = %d\n", nrow(dir), k, obs))
# Monte Carlo over the 2^k = 2^27 flips (too many to enumerate): 200,000 random flips, seed fixed
set.seed(20261117); B <- 200000
signs <- matrix(sample(c(-1, 1), B * k, replace = TRUE), B, k)
stat <- as.vector(signs %*% per_paper)
p_flip <- mean(abs(stat) >= abs(obs))
cat(sprintf("Monte Carlo two-sided paper-clustered sign-flip p = %.4f (%d of %d flips as extreme; MC SE %.4f)\n", p_flip,
            sum(abs(stat) >= abs(obs)), B, sqrt(p_flip * (1 - p_flip) / B)))
# control: a balanced per-paper vector must give p = 1
bal <- per_paper; bal[] <- 0
stopifnot(mean(abs(as.vector(signs %*% bal)) >= 0) == 1)
# unclustered reference: the registered exact binomial on the same 40 experiments
p40 <- binom.test(sum(dir$s == 1), nrow(dir))$p.value
cat(sprintf("unclustered reference (binomial) p = %.4f\n", p40))
cat("controls fired as expected\n")
