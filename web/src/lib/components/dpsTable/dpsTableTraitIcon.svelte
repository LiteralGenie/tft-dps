<script lang="ts">
    import type { GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { assetUrl } from '$lib/utils/networkUtils'

    let { trait, tier }: { trait: GameInfoValue['traits'][string]; tier: number } = $props()

    const variant: string = 'sm'
    const style: string = 'kBronze'
    const showHover = true

    // export let id: string
    // export let showHover = false
    // export let variant: 'sm' | 'md' = 'sm'
    // export let style: TraitIconStyle = null

    // $: src = TRAIT_ICONS[id]
</script>

<div class="flex flex-col items-center">
    <div
        class:sm={variant === 'sm'}
        class:md={variant === 'md'}
        class:bronze={style === 'kBronze'}
        class:silver={style === 'kSilver'}
        class:gold={style === 'kGold'}
        class:chromatic={style === 'kChromatic'}
        class:hover-layer={showHover}
        class="hex size-10!"
    >
        <div class="hex outline-layer">
            <div class="hex border-layer">
                <div class="hex bg-layer">
                    <img class="h-[66%] w-[66%]" src={assetUrl(trait.icon)} title={trait.name} />
                </div>
            </div>
        </div>
    </div>

    <span class="text-xs"> ({tier}) </span>
</div>

<style lang="postcss">
    .hex {
        @apply flex h-full w-full items-center justify-center;

        &.bg-layer {
            background-color: #131313;
        }

        &.outline-layer {
            background-color: rgba(0, 0, 0, 50%);
        }

        &.border-layer {
            background-color: #6b6d6b;
        }

        &.hover-layer {
            padding: 2.5px;
            cursor: pointer;

            &:hover,
            &:focus {
                filter: drop-shadow(0px 0px 20px rgba(255, 199, 46, 0.9));
            }
        }
    }

    .sm {
        & .outline-layer {
            padding: 2px;
        }
        & .border-layer {
            padding: 1px;
        }
    }

    .md {
        & .outline-layer {
            padding: 2px;
        }
        & .border-layer {
            padding: 1.5px;
        }
    }

    .hex.bronze {
        & .bg-layer {
            background: linear-gradient(#764a2c, #9c6442 40%, #57341b 60%, #57341b 100%);
        }

        & .border-layer {
            background-color: hsla(0, 0%, 100%, 50%);
        }
    }
    .hex.silver {
        & .bg-layer {
            background: linear-gradient(#738994, #a7bdc0 40%, #86a5a7 60%, #86a5a7 100%);
        }

        & .border-layer {
            background-color: hsla(0, 0%, 80%);
        }
    }
    .hex.gold {
        & .bg-layer {
            background: linear-gradient(#ddba53, #e7c360 40%, #af8528 60%, #af8528 100%);
        }

        & .border-layer {
            background-color: hsla(0, 0%, 80%);
        }
    }
    .hex.chromatic {
        /* This should never be used. Chromatic tiers aren't currently possible without emblems. */
        & .bg-layer {
            background: conic-gradient(
                #b8f9b8,
                #b0defe,
                #c1b9fc,
                #ef9eff,
                #aff7fe,
                #fafff3,
                #fffbbd,
                #f2b29c,
                #cceab3,
                #cbc9e9,
                #c5e0ff,
                #adffd8,
                #ffffd2,
                #9cfbff,
                #e6a7ff,
                #b8f9b8
            );
        }

        & .border-layer {
            background-color: hsla(0, 0%, 80%);
        }
    }

    .hex.bronze,
    .hex.silver,
    .hex.gold,
    .hex.chromatic {
        & img {
            filter: invert(1);
        }
    }
</style>
